"""
Data models
"""
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', _('Ativo')
        INACTIVE = 'inactive', _('Inativo')

    name = models.CharField(
        verbose_name=_('Nome'),
        max_length=64,
        null=True,
        blank=True
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
        null=True,
        blank=True,
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
        return self.device_eui


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

    mold_growth = models.FloatField(
        verbose_name=_('crescimento esperado de mofo'),
        null=True,
        blank=True,
    )

    payload = models.CharField(
        verbose_name=_('pacote de dados'),
        blank=True,
        null=True,
        max_length=4096,
    )

    date = models.DateTimeField(
        verbose_name=_('Data'),
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.device} - {self.date}'

    def save(self, *args, **kwargs):
        # Calculates the average measurements from past 7 days
        week_ago = timezone.now() - timezone.timedelta(days=7)
        measurements = Measurement.objects.filter(date__gte=week_ago).aggregate(
            Avg('humidity'), Avg('temperature'),)
        humidity_average = measurements.get('humidity__avg')
        temperature_average = measurements.get('temperature__avg')
        if humidity_average < 80.0:
            self.mold_growth = 0
        else:
            # Parameters taken from a linear regression
            self.mold_growth = (-6344.226743197284
                                + 79.29438776*humidity_average
                                + 6.259375*temperature_average)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Medição')
        verbose_name_plural = _('Medições')
