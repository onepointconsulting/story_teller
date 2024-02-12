import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    bearer_token = os.getenv("MY_MIDJOURNEY_BEARER_TOKEN", "")
    sleep_time = int(os.getenv("SLEEP_TIME", "10"))
    message_attempts = int(os.getenv("MESSAGE_ATTEMPTS", "30"))
    temp_dir_str = os.getenv("MY_MIDJOURNEY_TEMP_DIR", tempfile.gettempdir())
    temp_dir = Path(temp_dir_str)
    if not temp_dir.exists():
        temp_dir.mkdir(parents=True)


midjourney_cfg = Config()
