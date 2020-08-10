"""
Data models
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', _('Ativo')
        INACTIVE = 'inactive', _('Inativo')

    name = models.CharField(
        verbose_name=_('Nome'),
        max_length=64,
    )

    device_eui = models.CharField(
        verbose_name=_('EUI do Dispositivo'),
        max_length=64,
    )

    application_eui = models.CharField(
        verbose_name=_('EUI da Aplicação'),
        max_length=64,
        null=True,
    )

    status = models.CharField(
        verbose_name=_('Status'),
        max_length=16,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )

    owner = models.ForeignKey(
        User,
        verbose_name=_('Proprietário'),
        on_delete=models.CASCADE,
        related_name='devices',
    )

    created_at = models.DateTimeField(
        verbose_name=_('Data de criação'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_('Data de atualização'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Dispositivo')
        verbose_name_plural = _('Dispositivos')

    def __str__(self):
        return self.name


class Measurement(models.Model):
    device = models.ForeignKey(
        Device,
        verbose_name=_('Dispositivo'),
        on_delete=models.CASCADE,
        related_name='measurements',
    )

    date = models.DateTimeField(
        verbose_name=_('Data'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Medição')
        verbose_name_plural = _('Medições')
