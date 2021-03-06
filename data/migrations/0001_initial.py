# Generated by Django 3.1 on 2020-08-10 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Nome')),
                ('device_eui', models.CharField(max_length=64, verbose_name='EUI do Dispositivo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de atualização')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL, verbose_name='proprietário')),
            ],
        ),
    ]
