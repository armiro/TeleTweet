# import schedule
import asyncio, platform
from src.twitter_crawler import *
from src.telegram_poster import *


MEDIA_PATH = './media/'
TWT_CREDS_FILE = './twitter_creds.json'
TWT_USR_NAME = 'MariusCrypt0'
TLGM_CREDS_FILE = './telegram_creds.json'
TLGM_CHANNEL_ID = '@marius_kramer'

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def main():
    api = authenticate(creds_path=TWT_CREDS_FILE)
    timeline = api.user_timeline(screen_name=TWT_USR_NAME, count=100, exclude_replies=True, include_rts=True,
                                 tweet_mode='extended')
    admin = get_bot(creds_path=TLGM_CREDS_FILE)

    for status in timeline[1:2]:
        print('--------------------------------------')
        # print(status)
        is_retweet = status.full_text.startswith('RT')
        status_time = extract_status_time(status)
        tags, symbols = extract_tags_and_symbols(status, is_retweet=is_retweet)
        author_name = get_author_name(status, is_retweet=is_retweet)
        num_files = download_media(status, media_path=MEDIA_PATH, is_retweet=is_retweet)
        print('--------------------------------------')
        text = extract_and_polish_text(tweet=status, is_retweet=is_retweet)
        asyncio.run(post_tweet(bot=admin, channel_id=TLGM_CHANNEL_ID, time=status_time, author=author_name, text=text,
                               has_media=num_files))
        break


if __name__ == '__main__':
    main()
    # schedule.every().day.at("11:30").do(main)
    # while True:
    #   schedule.run_pending()
    #   time.sleep(1)

