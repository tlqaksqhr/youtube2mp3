from celery import Celery
from core import YoutubeConverter,DownloadAudioInfoDTO

from __future__ import absolute_import
from celery import shared_task

@shared_task
def download_action(video_url):
	conv = YoutubeConverter("downloads/")
	result = conv.convert_youtube(video_url)

	# add elasticsearch add value routine...
	download_dto = DownloadAudioInfoDTO()
	download_dto.insert(result["video_id"],result)