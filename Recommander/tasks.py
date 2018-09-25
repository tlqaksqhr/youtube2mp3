from celery import Celery
from core import YoutubeConverter

convertTask = Celery('tasks',broker='pyamqp://guest@localhost//')

@convertTask.task
def download_action(video_url):
	conv = YoutubeConverter("downloads/")
	result = conv.convert_youtube(video_url)