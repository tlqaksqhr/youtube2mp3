from pytube import YouTube,extract
from pytube.exceptions import RegexMatchError
import ffmpeg
import os
from pathlib import Path

from converter.coreconfig import CONFIG

from elasticsearch import Elasticsearch, NotFoundError


# TODO : additional implementation when exception case (not found youtube video, fail to convert mp4 -> mp3 : duplicate youtube file, race condition...) needed.

class YoutubeConverter():

	def __init__(self,download_path):
		self.download_path = download_path

	def convert_youtube(self,video_url):
		try:
			yt = YouTube(video_url)
			title = yt.title
			vid = extract.video_id(video_url)
		except RegexMatchError:
			return {}

		# TODO : addtional download url factory class is need. 
		download_url = "{}://{}/{}/{}".format(CONFIG['scheme'],CONFIG['host'],"download",vid)
		result = {"title" : title, "video_id" : vid, "download_url" : download_url}

		input_filename = "{}.{}".format(vid,"mp4")
		output_filename = "{}.{}".format(vid,"mp3")

		full_input_path = os.path.join(self.download_path,input_filename)
		full_output_path = os.path.join(self.download_path,output_filename)

		input_path_handle = Path(full_input_path)
		output_path_handle = Path(full_output_path)

		if input_path_handle.is_file() == False:
			yt.streams.filter(file_extension='mp4').first().download(self.download_path,vid)
		
		if output_path_handle.is_file() == False:
			stream = ffmpeg.input(full_input_path)
			stream = ffmpeg.output(stream, full_output_path)
			ffmpeg.run(stream)

		if input_path_handle.is_file():
			os.remove(full_input_path)

		return result

class DownloadAudioInfoDTO():

	def __init__(self):
		self.es = Elasticsearch()
		self.index = "youtube2mp3"
		self.doc_type = "downloadinfo"

	def insert(self,key,value):
		result = self.es.index(index=self.index, doc_type=self.doc_type, id=key, body=value)
		return result

	def search(self,key):
		result = self.es.get(index=self.index, doc_type=self.doc_type, id=key)
		if '_source' in result:
			return result['_source']
		else:
			result = {}
			return result




#conv = YoutubeConverter("downloads/")
#conv.convert_youtube("https://www.youtube.com/watch?v=1VrOqVKX2Nc")