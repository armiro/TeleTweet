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


async def post_tweet(bot, channel_id, time, author, text, has_media):
    """
    documentation: https://docs.python-telegram-bot.org/en/stable/telegram.bot.html
    :param bot: telegram bot
    :param channel_id: string
    :param time: string
    :param author: string
    :param text: string
    :param has_media: set(int, string)
    :return: None
    """
    full_text = f'{time} \n\n{author} \n\n{text}'
    if has_media[0]:
        await bot.send_photo(chat_id=channel_id, photo=has_media[1], caption=full_text)
    else:
        await bot.send_message(chat_id=channel_id, text=full_text)

