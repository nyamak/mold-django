# Generated by Django 3.1 on 2020-08-11 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_measurement_payload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='payload',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='pacote de dados'),
        ),
    ]
