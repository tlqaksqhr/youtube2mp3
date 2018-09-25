from tasks import download_action
import os

file_handle = open("urllist.txt")
urls = file_handle.read().split("\n")
dir_list = []

for dirName, subdirList, fileList in os.walk("downloads/"):
	dir_list = fileList

for url in urls:
	file_name = url.split("v=")[1][0:11] + ".mp3"
	if file_name not in dir_list:
		result = download_action.delay(url)