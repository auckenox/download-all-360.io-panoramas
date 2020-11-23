#!/usr/bin/env python
# -*- coding: utf-8 -*-

# purpose: download all flat images of one or more users from the 360.io gallery
# requirements: pip3 install requests
# github: https://github.com/auckenox/download-all-360.io-panoramas
# script version 0.3


# settings #################################################################################################################
user_urls = ['http://360.io/user/3ca6-11/vikas-reddy/'] # example: ['http://360.io/user/3ca6-11/vikas-reddy/']
target_path = '' # example: /path/to/existing-folder/ | must end with a slash | leave this empty to use path of this script
download_images = True # default: True | set this to False to just print out the image urls instead of downloading them
############################################################################################################################




try:
	import requests
except Exception as e:
	print('please install requests with this command: "pip3 install requests" and run this script again')
	sys.exit(1)

import re,time,sys,os


if target_path == '' and download_images:
	target_path = os.path.dirname(os.path.realpath(__file__))+"/"

if download_images and not os.path.isdir(target_path):
	print("please enter a valid/existing target_path.")
	sys.exit(1)

def getHtml(url):
	print("getHtml for url: "+url)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
	try:
		r = requests.get(url, headers=headers) # params={'s': thing}
		return r.text
	except requests.exceptions.Timeout:
		print("timeout!")
		# Maybe set up for a retry, or continue in a retry loop
	except requests.exceptions.TooManyRedirects:
		print("TooManyRedirects!")
		# Tell the user their URL was bad and try a different one
	except requests.exceptions.RequestException as e:
		# catastrophic error. bail.
		print("fatal error in getHtml: %s"%e)
		return False



def getImageList(html):
	regex = r"<div class=\"panoramarow\">\s*<a href=\"/(.*)\">"
	base_url = 'https://360.io/images/viewer/' # wUt2Rx_flat.jpg
	matches = re.finditer(regex, html, re.MULTILINE)
	url_list = []
	for matchNum, match in enumerate(matches, start=1):
		for groupNum in range(0, len(match.groups())):
			groupNum = groupNum + 1
			short_id = match.group(groupNum)
			#print(base_url+short_id+"_flat.jpg")
			url_list.append(base_url+short_id+"_flat.jpg")
	return url_list



def downloadImage(url,target_path):
	local_filename = target_path+url.split('/')[-1]
	if os.path.isfile(local_filename):
		print("skipping image "+local_filename+" because the file already exists")
		return True
	try:
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					# If you have chunk encoded response uncomment if
					# and set chunk_size parameter to None.
					#if chunk: 
					f.write(chunk)
		return local_filename
	except Exception as e:
		print('warning, download of image "%s" failed: %s'%(url,e))
		return False



def getLastPage(html):
	regex = r"<a href=\"/user/.*/.*/([0-9]*)/\"><span class= \"enabled\">Last</span></a>"
	matches = re.finditer(regex, html, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		for groupNum in range(0, len(match.groups())):
			groupNum = groupNum + 1
			last_page = match.group(groupNum)
			#print(last_page)
			return int(last_page)


for user_url in user_urls:
	page_url = '%s1/'%user_url
	#print("getting page count from user url now..")

	first_html = getHtml(user_url)
	last_page = getLastPage(first_html)
	print("there are %i pages for this user"%last_page)

	for paging_no in range(1,last_page+1):
		page_url = '%s%i/'%(user_url,paging_no)
		html = getHtml(page_url)
		#time.sleep(0.1)

		if download_images:
			print("#"*30+" page_url: "+page_url+" "+"#"*30)

		image_list = getImageList(html)
		for img_url in image_list:
			if download_images:
				#time.sleep(0.1)
				dl_name = downloadImage(img_url,target_path)
				if dl_name != True and dl_name != False:
					print("downloaded image to: "+dl_name)

			else:
				# do not download anything, just print all image urls
				print(img_url)


