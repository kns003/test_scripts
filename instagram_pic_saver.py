'''
Created on Apr 13, 2014

@author: shashank
'''

'''
This is a scripts which will save all the pics of a instagram user based on the username being
entered in the command line argument. To get the username, go to instagram.com and select ur friend whose pics have to be saved.
In the url 'intagram.com/<user_name>', will give you the username.
'''

import os
import sys
import requests
import json
import urllib
from urlparse import urlparse

#you can get this from 'http://instagram.com/developer/api-console/' and Authentication should be Oauth2
#Then type anything in the Request URL. You will receive the token in the Request Block
INSTAGRAM_ACCESS_TOKEN = ''
resp = requests.get('https://api.instagram.com/v1/users/search?q='+sys.argv[1]+'&access_token='+INSTAGRAM_ACCESS_TOKEN)
resp = json.loads(resp.text)
if resp['data'][0]['username'] == sys.argv[1]:
	user_id = str(resp['data'][0]['id'])
media_url = 'https://api.instagram.com/v1/users/'+user_id+'/media/recent?access_token='+INSTAGRAM_ACCESS_TOKEN
media_response = requests.get(media_url)
media_response = json.loads(media_response.text)

def save_pagination(media_response):
	try:
		next_page = str(media_response['pagination']['next_url'])
		next_page_json = requests.get(next_page)
		print next_page_json.content
		next_page_json = json.loads(next_page_json.text)
		save_photos(next_page_json)
	except Exception,e:
		print e

def save_photos(media_response):
	media_list = []
	for user_media in media_response['data']:
		media_list.append(user_media['images']['standard_resolution']['url'])
	#Specify the path required. for Eg : /home/Pictures/insta_pics. this is for linux users
	PATH = ''+sys.argv[1]
	if not os.path.exists(PATH):
		os.makedirs(PATH)
	for media in media_list:
		urllib.urlretrieve(str(media),PATH+str(urlparse(media).path))
		print 'saved'
	if media_response['pagination']:
		save_pagination(media_response)
	else:
		return False

save_photos(media_response)
