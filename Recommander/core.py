from pytube import YouTube,extract
import ffmpeg
import os

from elasticsearch import Elasticsearch


# TODO : additional implementation when exception case (not found youtube video, fail to convert mp4 -> mp3) needed.

class YoutubeConverter():

	def __init__(self,download_path):
		self.download_path = download_path

	def convert_youtube(self,video_url):
		yt = YouTube(video_url)
		title = yt.title
		vid = extract.video_id(video_url)

		yt.streams.filter(file_extension='mp4').first().download(self.download_path,vid)

		input_filename = "{}.{}".format(vid,"mp4")
		output_filename = "{}.{}".format(vid,"mp3")

		full_input_path = os.path.join(self.download_path,input_filename)
		full_output_path = os.path.join(self.download_path,output_filename)

		stream = ffmpeg.input(full_input_path)
		stream = ffmpeg.output(stream, full_output_path)
		ffmpeg.run(stream)

		os.remove(full_input_path)

		result = { "download_path" : full_output_path, "title" : title, "video_id" : vid}

		return result

#conv = YoutubeConverter("downloads/")
#conv.convert_youtube("https://www.youtube.com/watch?v=1VrOqVKX2Nc")

class DownloadAudioInfoDTO():

	def __init__(self):
		self.es = Elasticsearch()
		self.index = "youtube2mp3"
		self.doc_type = "downloadinfo"

	def insert(self,key,value):
		result = self.es.index(index=self.index, doc_type=self.doc_type, id=key, body=value)
		return result

	def search(self,key):
		result = self.es.get(index=self.index, doc_type=self.doc_type, id=key)['_source']
		return result
