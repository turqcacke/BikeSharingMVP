from datetime import datetime
import pytz
from django.db import models
from django.conf import settings
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import FieldError
import qrcode


class DefaultStatuses(models.IntegerChoices):
    OCCUPIED = 0
    AVAILABLE = 1
    MAINTENANCE = 2

    def __str__(self):
        return self.name


class OrderStatuses(models.IntegerChoices):
    PENDING = 0
    ACTIVE = 1
    FINISHED = 2

    def __str__(self):
        return self.name


class ActiveBikeManager(models.Manager):
    def get_queryset(self):
        return super(ActiveBikeManager, self).get_queryset().all().filter(status=1)


class StatusOneManager(models.Manager):
    def get_queryset(self):
        try:
            return super(StatusOneManager, self).get_queryset().all().filter(status=1)
        except FieldError:
            return super(StatusOneManager, self).get_queryset().all()


class StatusZeroManager(models.Manager):
    def get_queryset(self):
        try:
            return super(StatusZeroManager, self).get_queryset().all().filter(status=0)
        except FieldError:
            return super(StatusZeroManager, self).get_queryset().all()


class Order(models.Model):
    objects = models.Manager()
    active = StatusOneManager()
    id = models.IntegerField(primary_key=True)
    status = models.IntegerField(choices=OrderStatuses.choices, default=OrderStatuses.ACTIVE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    bike = models.ForeignKey('Bike', related_name='bike', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.bike:
            if self.status == 1 and not self.start:
                self.start = datetime.now(tz=pytz.timezone('Asia/Tashkent'))
                self.bike.status = 0
                self.bike.save()
            elif self.status == 2 and not self.end:
                self.end = datetime.now(tz=pytz.timezone('Asia/Tashkent'))
                self.bike.status = 1
            self.bike.save()
        super(Order, self).save()


class Station(models.Model):
    objects = models.Manager()
    free = StatusOneManager()
    occupied = StatusZeroManager()
    id = models.IntegerField(primary_key=True)
    status = models.IntegerField(choices=DefaultStatuses.choices, default=DefaultStatuses.AVAILABLE)
    longitude = models.FloatField(blank=True)
    latitude = models.FloatField(blank=True)
    max_bike_place = models.IntegerField()

    def __str__(self):
        return '{} | {}'.format(self.id, DefaultStatuses(self.status).name)


class BikePlace(models.Model):
    objects = models.Manager()
    id = models.IntegerField(primary_key=True)
    status = models.IntegerField(choices=DefaultStatuses.choices, default=DefaultStatuses.AVAILABLE)
    station = models.ForeignKey(Station, related_name='bike_place', on_delete=models.CASCADE)
    bike = models.OneToOneField('Bike', related_name='bike_place', on_delete=models.SET_NULL, null=True)
    qrcode = models.ImageField(upload_to='stations/qr/', blank=True)

    def save(self, *args, **kwargs):
        if not self.qrcode:
            qr = qrcode.make(str(self.id))
            # + ';' + str(self.station.id)).get_image().convert("RGB")
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            self.qrcode.save(name=str(self.station.id) + '/' + f'{self.id}.png',
                             content=InMemoryUploadedFile(buffer,
                                                          None,
                                                          'code.png',
                                                          'image/png',
                                                          buffer.tell(),
                                                          None),
                             save=True
                             )
        super(BikePlace, self).save(*args, **kwargs)

    def __str__(self):
        return '{} | {}'.format(self.id, DefaultStatuses(self.status).name)


class Bike(models.Model):
    objects = models.Manager()
    active = ActiveBikeManager()
    id = models.IntegerField(primary_key=True)
    status = models.IntegerField(choices=DefaultStatuses.choices, default=DefaultStatuses.AVAILABLE)

    def __str__(self):
        return '{} | {}'.format(self.id, DefaultStatuses(self.status).name)
