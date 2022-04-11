import numpy as np
import os
import time
import schedule


class TeleTweet:
  def __init__(self, twitter_id, telegram_channel, include_retweets=True, include_comments=False):
    self.twitter_id = twitter_id
    self.telegram_channel = channel
  
  def get_twitter_creds(usr, pwd):
    pass
  
  def crawl_recent_tweets(self.twitter_id):
    pass
  
  def get_telegram_creds(usr, pwd):
    pass
  
  def post(self.telegram_channel):
    pass
 

def main()
  bot = TeleTweet(twitter_id='elonmusk', telegram_channel='elonmuskfans')
  bot.ger_twitter_creds(usr='xyz', pwd='***')
  res = bot.crawl_recent_tweets()
  bot.get_telegram_creds(usr='xyz', pwd='***')
  bot.post()


if __name__ == '__main__':
  schedule.every().day.at("11:30").do(main)
  while True:
    schedule.run_pending()
    time.sleep(1)

