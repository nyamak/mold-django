"""
Data models
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    name = models.CharField(
        verbose_name=_('Nome'),
        max_length=64,
    )

    device_eui = models.CharField(
        verbose_name=_('EUI do Dispositivo'),
        max_length=64,
    )

    owner = models.ForeignKey(
        User,
        verbose_name=_('proprietário'),
        on_delete=models.CASCADE,
        related_name='devices',
    )

    created_at = models.DateTimeField(
        verbose_name=_('data de criação'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_('data de atualização'),
        auto_now=True,
    )

    def __str__(self):
        return self.name
