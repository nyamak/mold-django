import base64
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from data import models


@csrf_exempt
def receive_data(request):
    try:
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
