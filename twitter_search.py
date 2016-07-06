import urllib
import webbrowser

import requests
from bs4 import BeautifulSoup

# ACTUAL URL FROM TWITTER --  f : for tweets only q: search query, language, location and time_range, :) and :( for sentiments include:retweets for retweets
# https://twitter.com/search?f=tweets&q=tw lang:hi near:"New Delhi, India" within:15mi since:2016-04-20 until:2016-04-22 :) :( ? include:retweets&src=typd

urls = {
    'BASE_URL': 'https://www.twitter.com',
    'SEARCH_URL': 'https://www.twitter.com/search'
}

language_parms = {
    'hindi': 'hi',
    'french': 'fr',
    'english': 'en',
    'german': 'gr',
    'any': ''
}


def url_builder(search_type='tweets', search_query='', language='en', location='New Delhi, India',
                location_range='125mi', start_time='', end_time='', include_retweets=True, positive=False, questions='',
                negative=False, limit=10, media=False):
    params = {
        'f': search_type,
        'q': '',
        'src': 'typd'
    }
    if media:
        search_query += ' filter:media'

    search_query_params = {
        'lang': language
    }

    if location:
        search_query_params['near'] = '\"' + location + '\"'
    if location_range:
        search_query_params['within'] = location_range
    if start_time:
        search_query_params['since'] = start_time
    if end_time:
        search_query_params['until'] = end_time
    if include_retweets:
        search_query_params['include'] = 'retweets'

    query_string = ''
    for key, value in search_query_params.iteritems():
        query_string += key + ':' + value + ' '

    if positive:
        query_string += ':) '
    if negative:
        query_string += ':( '
    if questions:
        query_string += '? '
    if search_query:
        query_string += search_query

    params['q'] = query_string
    final_url = urls['SEARCH_URL'] + '?' + urllib.urlencode(params)
    
    return final_url


def get_page_content(url):
    req = requests.get(url)
    if req.status_code == 200:
        return req.text
    else:
        raise "Request not fulfilled"


def extract_tweets(html,media=False):
    tweets = []
    soup = BeautifulSoup(html, 'html.parser')
    write_to_file('soup.txt', soup)
    tweets_soup = soup.find_all('li', attrs={'data-item-type': 'tweet'})

    for tweet in tweets_soup:
        tweet_tuple = ()
        try:
            tweet_text = tweet.find('p', class_='tweet-text').get_text()
            author_link = urls['BASE_URL'] + tweet.find('a', class_='js-user-profile-link').get('href')
            author_avatar = tweet.find('img', class_='avatar').get('src')
            media_link = ''
            if media:
                media_link = tweet.find('div', class_='AdaptiveMedia-photoContainer').get('data-image-url')
                print media_link
            tweet_tuple = (author_link, author_avatar, tweet_text, media_link)
        except:
            pass
        tweets.append(tweet_tuple)

    with open('crux.txt', 'w') as file:
        file.write('\n\n*********Tweet*******\n'.join(' ||  '.join(tweet) for tweet in tweets).encode('utf-8'))
    webbrowser.open("crux.txt")

    return tweets


def find_trending_hashtags():
    soup = BeautifulSoup(get_page_content('http://trends24.in/india/'), 'html.parser')
    write_to_file('soup2.txt', soup)
    trending_hashtags = []
    trending_list_soup = soup.find('ol', class_='trend-card__list')
    for list_item in trending_list_soup.find_all('a'):
        trending_hashtags.append(list_item.get_text())
    return trending_hashtags


def write_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data.encode('utf-8'))


def count_occurences(data, word):
    words = data.split()
    return words.count(word)

def get_tweets(keywords, media=False):
    search_query = ' '.join(keywords)

    html = get_page_content(url_builder(search_query=search_query, media=media))
    tweets = extract_tweets(html, media=media)
    return tweets


def main():
    print 'Welcome To Twhitter'
    print 'Fetching what\'s trending on twitter...'
    trending = find_trending_hashtags()
    if trending:
        print 'Here \'s some of the hot topics right now'
        for trend in trending:
            print trend
    # search_query = raw_input('What tweets are you looking for?\n -->')
    # language = raw_input('Language Preference \n Hindi \t English(default) \t French \t German \Any \n -->').lower()
    # nature = raw_input('''What kind of tweets would you like to see?
    # \n Optimistic \t Pessimistic \t Inquisitive \t Any''').lower()
    # if nature == 'any':
    #     nature = ''
    # language = language_parms[language]
    # html = get_page_content(url_builder(search_query=search_query, language=language, positive='optimistic' in nature,
    #                                     negative='pessimistic' in nature, questions='inquisitive' in nature))
    html = get_page_content(url_builder(search_query='Pistorius', media=True))
    #print 'Extracting tweets ...'
    tweets = extract_tweets(html, media=True)
    #print 'Total Tweets Found :', len(tweets)

