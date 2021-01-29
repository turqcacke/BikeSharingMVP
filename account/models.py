from django.db import models
from django.conf import settings


class Balance(models.Model):
    class Status(models.IntegerChoices):
        BLOCKED = 0
        ACTIVE = 1

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='balance')
    card_number = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return str(self.balance) if self.status == self.Status.ACTIVE else self.Status.BLOCKED.name
