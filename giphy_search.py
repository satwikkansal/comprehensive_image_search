from giphypop import Giphy

def giphy_search(keywords):
	g = Giphy()
	query = ' '.join(keywords)
	results = [x.media_url for x in g.search(query)]
	return results