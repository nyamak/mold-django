"""
Data models
"""
from django.contrib.auth.models import User
from django.core import validators
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

    latitude = models.FloatField(
        verbose_name=_('latitude'),
        blank=True,
        null=True,
        validators=[
            validators.MinValueValidator(-90.0),
            validators.MaxValueValidator(90.0),
        ]
    )

    longitude = models.FloatField(
        verbose_name=_('longitude'),
        blank=True,
        null=True,
        validators=[
            validators.MinValueValidator(-180.0),
            validators.MaxValueValidator(180.0),
        ]
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

    humidity = models.FloatField(
        verbose_name=_('umidade'),
        null=True,
    )

    temperature = models.FloatField(
        verbose_name=_('temperatura'),
        null=True,
    )

    payload = models.CharField(
        verbose_name=_('pacote de dados'),
        blank=True,
        null=True,
        max_length=256,
    )

    date = models.DateTimeField(
        verbose_name=_('Data'),
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.device} - {self.date}'

    class Meta:
        verbose_name = _('Medição')
        verbose_name_plural = _('Medições')
