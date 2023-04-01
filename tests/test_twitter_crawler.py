import os
import pytest
from src.twitter_crawler import *


class TestAuthenticate:

    @pytest.fixture()
    def creds_path(self):
        return './twitter_creds.json'

    def test_creds_file_exits(self, creds_path):
        assert os.path.exists(creds_path), "Credentials file does not exist"

    def test_authenticate_returns_api_object(self, creds_path):
        api = authenticate(creds_path)
        assert api is not None, "API object is None"

    def test_authenticate_uses_tweepy(self, creds_path):
        api = authenticate(creds_path)
        assert api.user_agent.find('Tweepy') != -1, "API is not properly initiated"


