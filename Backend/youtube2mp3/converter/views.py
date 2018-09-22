from django.shortcuts import render
from django.http import HttpResponse,Http404

from django.views.decorators.csrf import csrf_exempt

from django.utils.encoding import smart_str
from django.http import JsonResponse

from converter import core
from converter.coreconfig import CONFIG
from converter.corelib import DownloadAudioInfoDTO

import re,os,json
from urllib.parse import quote



@csrf_exempt
def convert(request):
    if request.method == 'POST':
        result = core.convert_action(request.body.decode('utf-8'))
        return JsonResponse(result)
    else:
        return JsonResponse({"status" : "NOT-IMPLEMENTED!"})


def download_link(request,video_id):
    result = core.download_link_action(video_id)
    return JsonResponse(result)


def download(request,video_id):

    file_name = "{}.{}".format(video_id,"mp3")
    file_path = os.path.join(CONFIG['path'], file_name)
    video_id_pattern = re.compile("[a-zA-Z0-9\_\-]{11,11}")

    if os.path.exists(file_path) and video_id_pattern.match(video_id):
        download_dto = DownloadAudioInfoDTO()
        mp3_title = "{}.{}".format(download_dto.search(video_id)['title'],"mp3")
        mp3_title = mp3_title.replace(" ","_").encode('utf-8')

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            print(mp3_title)
            response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(quote(mp3_title))
            return response
    
    raise Http404