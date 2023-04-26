import tweepy
import json
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
    return tweet.created_at.strftime('%a, %d/%b/%Y, %H:%M %Z')


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


def download_media(tweet, media_path, is_retweet):
    if is_retweet:
        try:
            media_files = tweet.retweeted_status.extended_entities.get('media', [])
        except AttributeError:
            media_files = tweet.retweeted_status.entities.get('media', [])
    else:
        try:
            media_files = tweet.extended_entities.get('media', [])
        except AttributeError:
            media_files = tweet.entities.get('media', [])

    for idx, media_file in enumerate(media_files):
        media_type = media_file.get('type', [])
        if media_type == 'video' or media_type == 'animated_gif':
            media_url = media_file['video_info']['variants'][0]['url']
        else:
            media_url = media_file['media_url']
        media_name = tweet.id_str + '_' + str(idx) + media_url[media_url.rfind('.'):]
        _ = wget.download(url=media_url, out=media_path + media_name)
        print(f'downloaded media file no. {idx+1} successfully!')

    if not(len(media_files)): print('no downloadable media files found!')
    return (0, None, None) if not(len(media_files)) else (len(media_files), media_type, media_path+media_name)


def get_author_name(tweet, is_retweet):
    if is_retweet:
        author_name = tweet.entities.get('user_mentions')[0].get('name')
        author_handle = tweet.entities.get('user_mentions')[0].get('screen_name')
        rt_or_qt = 'QT' if tweet.is_quote_status else 'RT'
        return f'[{rt_or_qt}] {author_name} <a href="https://twitter.com/{author_handle}">@{author_handle}</a>'
    else:
        return f'{tweet.author.name} <a href="https://twitter.com/{tweet.author.screen_name}">@{tweet.author.screen_name}</a>'


def extract_full_text(tweet, is_retweet):
    return tweet.retweeted_status.full_text if is_retweet else tweet.full_text


def append_tweet_link(tweet_text):
    print(tweet_text)

