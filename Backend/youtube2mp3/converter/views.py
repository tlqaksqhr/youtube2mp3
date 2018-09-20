from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from converter import core

@csrf_exempt
def convert(request):

    if request.method == 'POST':
        result = core.convert_action(request.body.decode('utf-8'))
        return JsonResponse(result)
    else:
        return HttpResponse("NOT IMPLEMENTED!")

def download(request):
    return HttpResponse("Download page...")
