import os.path
import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import os
from hashlib import sha1   
import random
import re
from time import sleep

save_path = '/home/mathuryash5/6th Sem/Natural Language Processing/Project/Data/'

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')


user_agents = [
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
		'Opera/9.25 (Windows NT 5.1; U; en)',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
		'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
proxies = [{"http": "http://107.170.13.140:3128"}, {"http": "http://198.23.67.90:3128"}]

def url_to_filename(url):
	#Make a URL into a file name, using SHA1 hashes. 

	# use a sha1 hash to convert the url into a unique filename
	hash_file = sha1(url.encode('utf-8')).hexdigest() + '.html'
	return os.path.join(CACHE_DIR, hash_file)


def store_local(url, content):
	 #Save a local copy of the file.

	# If the cache directory does not exist, make one.
	if not os.path.isdir(CACHE_DIR):
		os.makedirs(CACHE_DIR)

	# Save to disk.
	local_path = url_to_filename(url)
	with open(local_path, 'wb') as f:
		f.write(content)


def load_local(url):
	   # Read a local copy of a URL.
	local_path = url_to_filename(url)
	if not os.path.exists(local_path):
		return None

	with open(local_path, 'rb') as f:
		return f.read()


# function to download the lyrics 
def get_lyric_AZ(url, proxies, user_agents):

	if load_local(url):
		print("i was here ---------------------------\n\n")
		soup = BeautifulSoup(load_local(url), 'lxml')
		# get the goods (which is the tag where the lyrics text is there)
		for goods in soup.find_all("div", {"class":None}):
			if len(goods.text) == 0: 
				continue
			return goods.text
	else:
		print('ooooooooooooooooooooooooooooooooooo\n\n')
		# so that the server doesn't understand it's a bot scraping
		sleep(random.randint(0,20))
		# get request with headers --> from the array and proxies --> from another array to prevent bot from getting blocked
		response = requests.get(url, headers = {'User-Agent': random.choice(user_agents)}, proxies = random.choice(proxies))
		# store the response and it's contents in the form of url, so that you don't repeat scraping by checking in local folder
		store_local(url, response.content)
		soup = BeautifulSoup(response.content, 'lxml')
		tmp = ""
		# get the goods (which is the tag where the lyrics text is there)
		for goods in soup.find_all("div", {"class":None}):
			if len(goods.text) == 0:
				print("hello asdgggggggggggggggggggggggggggggg") 
				continue
			return goods.text

def main():
	print("Welcome to main !  ! ! ! ")
	# read the song data from JSON, save song name and artist name to parse the url for get request 
	with open('run_results.json') as data_file:
		data = json.load(data_file)
		for song_data in data["selection1"]: 
			song_name = song_data["song_name"]
			artist = song_data["artist"]
			new_artist = artist.replace(" ","")
			new_song_name = song_name.replace(" ","")
			new_artist = new_artist.replace("\'","")
			new_song_name = new_song_name.replace("\'","")
			l_song = new_song_name.lower()
			l_artist = new_artist.lower()
			print(l_artist,l_song) 

			
			if(l_artist == "thewho"):
				l_artist="who"
			elif(l_artist == "rarycharles"):
				l_song="whatdisayparts12"
			# parsing the url to form the request
			url = "https://www.azlyrics.com/lyrics/"+l_artist+"/"+l_song+".html"
			print("\nURL_SONG =",url)
			# get lyrics from the function
			goodies = get_lyric_AZ(url,proxies,user_agents)
			if(goodies is None):
				continue
			complete_name = os.path.join(save_path,l_song+".txt") #parsing the path and name of the songs
			file = open(complete_name,"w")
			file.write(goodies)
			print("Successfully scraped song :",(l_song))
			file.close()

main()
	