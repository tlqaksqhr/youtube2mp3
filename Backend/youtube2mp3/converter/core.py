from elasticsearch import NotFoundError
from converter.corelib import DownloadAudioInfoDTO

from converter.tasks import convert_youtube_video
import json

def convert_action(request_data):
    data = json.loads(request_data)

    if 'url' in data:
        url = data['url']
        convert_youtube_video.delay(url)
        result = {"status" : "ok"}
    else:
        result = {"status" : "fail"}

    return result

def download_link_action(video_id):
    try:
        audio_dto = DownloadAudioInfoDTO()
        result = audio_dto.search(video_id)

        if result == {}:
            result['status'] = 'failed'
        else:
            result['status'] = 'success'
    except NotFoundError:
        result = {}
        result['status'] = 'failed'
    return result