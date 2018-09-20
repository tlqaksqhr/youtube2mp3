from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def convert(request):

    if request.method == 'POST':
        return HttpResponse(request.body.decode('utf-8'))
    else:
        return HttpResponse("Convert page...")

def download(request):
    return HttpResponse("Download page...")
