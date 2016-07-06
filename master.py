from twitter_search import get_tweets, find_trending_hashtags
from Bing_Image_search import bing_search
from giphy_search import giphy_search
from google_search import google_search


def main():
	query_string = raw_input("Enter keywords seperated by space \n -->")
	keywords = query_string.split(' ')

	print 'Performing Bing search...'
	bing_images_links = [image['url'] for image in bing_search(keywords)]
	print 'Done.'
	
	print 'Performing Giphy search...'
	gifs_links = giphy_search(keywords)

	print 'Performing Google search...'
	google_images_links = google_search(keywords)

	print 'Performing Twitter tweets search...'

	twitter_text = [tweet[2] for tweet in get_tweets(keywords, media=False)]
	

	print 'Performing Twitter media search...'
	twitter_images_links = []
	try:
		for tweet in get_tweets(keywords, media=True):
			if len(tweet)==4:
				twitter_images_links.append(tweet[3])
	except:
		pass

	print 'Done performing searches.'

	print 'Printing out the results'

	print_links('Bing', bing_images_links)
	print_links('Giphy', gifs_links)
	print_links('Google', google_images_links)
	print_links('Twitter', twitter_text)
	print_links('Twitter Media', twitter_images_links)

def print_links(source, links):
	print 'Priinting Results from', source
	for i in range(len(links)):
		print i,'.\t',links[i]



















if __name__ == "__main__":
    main()