import base64
import json

from django.db.models import Avg
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from data import models


@csrf_exempt
def receive_data(request):
    try:
        if models.Measurement.objects.filter(payload__exact=request.body).exists():
            raise Exception('Duplicate payload')
        payload = json.loads(request.body)
        meta = payload.get('meta')
        device, _ = models.Device.objects.get_or_create(
            device_eui=meta.get('device'),
            application_eui=meta.get('application'),
        )
        params = payload.get('params')
        decoded_data = base64.b64decode(params.get('payload')).hex()
        temperature = int(decoded_data[0:2], 16) + int(decoded_data[2:4], 16)/10
        humidity = int(decoded_data[4:6], 16) + int(decoded_data[6:8], 16)/10
        measurement = models.Measurement.objects.create(
            device=device,
            payload=request.body,
            temperature=temperature,
            humidity=humidity,
        )
        return HttpResponse(status=204)
    except BaseException:
        return HttpResponse(status=400)


@csrf_exempt
def device_dashboard(request, device_eui):
    queryset = models.Measurement.objects.filter(device__device_eui=device_eui).order_by('date')

    week_ago = timezone.now() - timezone.timedelta(days=7)
    measurements = list(models.Measurement
                        .objects
                        .filter(temperature__isnull=False, humidity__isnull=False, device__device_eui=device_eui,
                                date__gte=week_ago)
                        .values(trunc_date=TruncDate('date'))
                        .annotate(Avg('temperature'), Avg('humidity'), Avg('mold_growth'))
                        .order_by('trunc_date'))
    labels = [str(day.get('trunc_date')) for day in measurements]
    temp_data = [day.get('temperature__avg') for day in measurements]
    hum_data = [day.get('humidity__avg') for day in measurements]
    growth_data = [day.get('mold_growth__avg') if isinstance(day.get('mold_growth__avg'), float) else 0 for day in measurements]

    latest_measurement = queryset.last()
    return render(request, 'data/dashboard.html', context={
        'latest_measurement': latest_measurement,
        'labels': labels,
        'temp_data': temp_data,
        'hum_data': hum_data,
        'growth_data': growth_data,
    })
