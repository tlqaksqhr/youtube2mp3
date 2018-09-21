from __future__ import absolute_import

from celery import Celery
from converter.corelib import YoutubeConverter,DownloadAudioInfoDTO

from converter.coreconfig import CONFIG

from celery import shared_task

# TODO : nofify that youtube conversion is success or fail to client

@shared_task
def convert_youtube_video(video_url):

	conv = YoutubeConverter(CONFIG['path'])
	result = conv.convert_youtube(video_url)

	if "video_id" in result:
		download_dto = DownloadAudioInfoDTO()
		download_dto.insert(result["video_id"],result)