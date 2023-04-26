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
        print(f'downloaded media file no. {idx + 1} successfully!')

    if not (len(media_files)): print('no downloadable media files found!')
    return (0, None, None) if not (len(media_files)) else (len(media_files), media_type, media_path + media_name)


def get_author_name(tweet, is_retweet):
    if is_retweet:
        author_name = tweet.entities.get('user_mentions')[0].get('name')
        author_handle = tweet.entities.get('user_mentions')[0].get('screen_name')
        return f'[RT] {author_name} <a href="https://twitter.com/{author_handle}">@{author_handle}</a>'
    elif tweet.is_quote_status:
        return f'[QT from {tweet.quoted_status.user.name} <a href="https://twitter.com/{tweet.quoted_status.user.screen_name}">@{tweet.quoted_status.user.screen_name}</a>]'
    else:
        return f'{tweet.author.name} <a href="https://twitter.com/{tweet.author.screen_name}">@{tweet.author.screen_name}</a>'


def extract_and_polish_text(tweet, is_retweet):
    full_text = tweet.retweeted_status.full_text if is_retweet else tweet.full_text  # extract full text
    urls = tweet.retweeted_status.entities.get('urls', [])
    media_urls = tweet.retweeted_status.entities.get('media', [])

    for idx, url_dict in enumerate(urls):  # replace links with embedded hyperlinks
        if full_text.find(url_dict['url']) >= 0:
            full_text = full_text.replace(url_dict['url'], f'\n\n<a href="{urls[idx]["expanded_url"]}">link</a>')
    for url_dict in media_urls:  # remove links to attached media
        if full_text.find(url_dict['url']) >= 0:
            full_text = full_text.replace(url_dict['url'], '')

    return full_text
