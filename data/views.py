import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from data import models


@csrf_exempt
def receive_data(request):
    device = models.Device.objects.first()
    payload = request.body
    try:
        measurement = models.Measurement.objects.create(device=device, payload=payload)
        return HttpResponse(status=204)
    except KeyError:
        return HttpResponse(status=400)
