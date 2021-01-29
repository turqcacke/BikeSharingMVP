from django.db import models
from django.conf import settings


class Status(models.IntegerChoices):
    BLOCKED = 0
    ACTIVE = 1


class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='balance')
    card_number = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return str(self.balance) if self.status == Status.ACTIVE else Status.BLOCKED.name
