import tweepy
import json
import numpy as np
import pandas as pd
from PIL import Image
import wget


def authenticate(creds_path):
    """
    read the credentials and authenticate to Twitter
    :param creds_path: str, containing path to credentials file
    :return: api, the authenticated API object
    """
    with open(creds_path, mode='r') as f: creds = json.load(f)
    C_KEY, C_SECRET = creds['api_key'], creds['api_key_secret']
    A_TOKEN, A_TOKEN_SECRET = creds['access_token'], creds['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key=C_KEY, consumer_secret=C_SECRET)
    auth.set_access_token(key=A_TOKEN, secret=A_TOKEN_SECRET)
    api = tweepy.API(auth=auth, wait_on_rate_limit=True)
    return api


def extract_status_time(tweet):
    return tweet.created_at.strftime('%a, %d/%B/%Y, %H:%M %Z')


def extract_tags_and_symbols(tweet, is_retweet):
    if is_retweet:
        tags = tweet.retweeted_status.entities['hashtags']
        symbols = tweet.retweeted_status.entities['symbols']
    else:
        tags = tweet.entities['hashtags']
        symbols = tweet.entities['symbols']
    tags = ['#' + tag['text'] for tag in tags]
    symbols = ['$' + symbol['text'] for symbol in symbols]
    return tags, symbols


def download_media(tweet, is_retweet):
    if is_retweet:
        media_files = tweet.retweeted_status.entities.get('media', [])
    else:
        media_files = tweet.entities.get('media', [])

    for idx, media_file in enumerate(media_files):
        media_url = media_file['media_url']
        media_name = tweet.id_str + '_' + str(idx) + media_url[media_url.rfind('.'):]
        img = wget.download(url=media_url, out=media_name)
        print(f'downloded image no. {idx+1} successfully!')

    if not(len(media_files)): print('no downloadable images found!')
    return None


def print_author(tweet, is_retweet):
    if is_retweet:
        original_author_name = tweet.entities.get('user_mentions')[0].get('name')
        original_author_handle = tweet.entities.get('user_mentions')[0].get('screen_name')
        print('RT:', original_author_name + ' @' + original_author_handle)
    else:
        print('Originally tweeted by:', tweet.author.name + ' @' + tweet.author.screen_name)
    return None


def extract_full_text(tweet, is_retweet):
    return tweet.retweeted_status.full_text if is_retweet else tweet.full_text


def main():
    USR_NAME = 'MariusCrypt0'
    api = authenticate(creds_path='../twitter_creds.json')
    timeline = api.user_timeline(screen_name=USR_NAME, count=50, exclude_replies=True, include_rts=True,
                                 tweet_mode='extended')

    for status in timeline:
        print('--------------------------------------')
        is_retweet = status.full_text.startswith('RT')
        status_time = extract_status_time(status)
        print('tweet posted at: ', status_time)
        tags, symbols = extract_tags_and_symbols(status, is_retweet=is_retweet)
        print('tweet has these tags:', tags)
        print('tweet has these symbols:', symbols)
        print_author(status, is_retweet=is_retweet)
        text = extract_full_text(status, is_retweet=is_retweet)
        print('full tweet text: \n', text)
        download_media(status, is_retweet=is_retweet)
        print('--------------------------------------')
        break


if __name__ == '__main__':
    main()
