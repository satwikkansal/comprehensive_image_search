# import urllib2
# import simplejson
# import cStringIO

# fetcher = urllib2.build_opener()
# searchTerm = 'parrot'
# startIndex = 0
# searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + 'Rahul Dravid' + "&start=" + str(startIndex)
# f = fetcher.open(searchUrl)
# deserialized_output = simplejson.load(f)

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os


def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

def google_search(keywords):
	search_query = ('+').join(keywords)
	image_type = "Action"

	url="https://www.google.co.in/search?q="+search_query+"&source=lnms&tbm=isch"
	
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)

	images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
	return images
	#print images
	# for img in images:
	#   raw_img = urllib2.urlopen(img).read()
	#   #add the directory for your image here 
	#   print img
	#   # DIR="C:\Users\hp\Pictures\\valentines\\"
	  # cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
	  # print cntr
	  # f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
	  # f.write(raw_img)
	  # f.close()