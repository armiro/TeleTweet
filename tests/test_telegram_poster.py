import os
import pytest
from src.telegram_poster import *


class TestGetBotUrl:

    @pytest.fixture()
    def creds_path(self):
        return './telegram_creds.json'

    def test_creds_file_exits(self, creds_path):
        assert os.path.exists(creds_path), "Credentials file does not exist"

    def test_url_is_str(self, creds_path):
        bot_url = get_bot_url(creds_path)
        assert isinstance(bot_url, str), "Returning URL is not a string"


class TestGetBot:

    @pytest.fixture()
    def creds_path(self):
        return './telegram_creds.json'

    def test_creds_file_exits(self, creds_path):
        assert os.path.exists(creds_path), "Credentials file does not exist"

    def test_get_bot_returns_api_object(self, creds_path):
        bot = get_bot(creds_path)
        assert bot is not None, "API object is None"

