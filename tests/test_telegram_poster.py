import os
import pytest
from src.telegram_poster import *


class TestGetBot:

    @pytest.fixture()
    def creds_path(self):
        return './telegram_creds.json'

    def test_creds_file_exits(self, creds_path):
        assert os.path.exists(creds_path), "Credentials file does not exist"

