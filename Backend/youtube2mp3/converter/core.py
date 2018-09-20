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

def download_action():
    pass