import os

import pytest
from src.twitter_crawler import *


def test_creds_file_exits(creds_path='./twitter_creds.json'):
    assert os.path.exists(creds_path), "Credentials file does not exist"


def test_authenticate():
    result = authenticate(creds_path='./twitter_creds.json')
    assert result.user_agent.find('Tweepy') != -1




