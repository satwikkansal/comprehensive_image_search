from py_bing_search import PyBingImageSearch as pbis 

def bing_search(keywords,limit=10):
	API_KEY = 'YOUR_API_KEY'
	search_query = (' ').join(keywords)
	image_filters = image_filters='Size:medium' #optional
	bi = pbis(API_KEY, search_query)
	search_results = bi.search(limit=limit, format='json')

	images = []

	for image in search_results:
		url = image.media_url
		title = image.title
		source_url = image.source_url
		#TODO: Traceback source_url to get the Title of source page.
		images.append({'title':title, 'url':url, 'source':source_url})
		#images.append(url)
	return images

