import json
import telegram


def get_bot_url(creds_path):
    with open(creds_path, mode='r') as f: creds = json.load(f)
    api_token, chat_id = creds['api_token'], creds['chat_id']
    url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chat_id}"
    return url


def get_bot(creds_path):
    with open(creds_path, mode='r') as f: creds = json.load(f)
    api_token = creds['api_token']
    return telegram.Bot(token=api_token)


async def post_tweet(bot, channel_id, time=None, tags=None, symbols=None, author=None, text=None, attachments=None):
    await bot.send_message(chat_id=channel_id, text=time)
    await bot.send_message(chat_id=channel_id, text=text)

