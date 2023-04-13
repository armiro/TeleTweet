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


def download_media(tweet, media_path, is_retweet):
    if is_retweet:
        media_files = tweet.retweeted_status.extended_entities.get('media', [])
    else:
        media_files = tweet.extended_entities.get('media', [])
    for idx, media_file in enumerate(media_files):
        if media_file.get('type', []) == 'video':
            media_url = media_file['video_info']['variants'][0]['url']
            print(media_file['video_info']['variants'][0])
        else:
            media_url = media_file['media_url']
        media_name = tweet.id_str + '_' + str(idx) + media_url[media_url.rfind('.'):]
        # print(media_name)
        # _ = wget.download(url=media_url, out=media_path + media_name)
        # print(f'downloaded image no. {idx+1} successfully!')

    if not(len(media_files)): print('no downloadable images found!')
    return (0, None) if not(len(media_files)) else (len(media_files), media_path+media_name)


def get_author_name(tweet, is_retweet):
    if is_retweet:
        original_author_name = tweet.entities.get('user_mentions')[0].get('name')
        original_author_handle = tweet.entities.get('user_mentions')[0].get('screen_name')
        return f'RT from: {original_author_name} @{original_author_handle}'
    else:
        return f'Tweeted by: {tweet.author.name} @{tweet.author.screen_name}'


def extract_full_text(tweet, is_retweet):
    return tweet.retweeted_status.full_text if is_retweet else tweet.full_text




