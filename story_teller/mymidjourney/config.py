import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    bearer_token = os.getenv("MY_MIDJOURNEY_BEARER_TOKEN", "")
    sleep_time = int(os.getenv("SLEEP_TIME", "10"))
    message_attempts = int(os.getenv("MESSAGE_ATTEMPTS", "10"))


midjourney_cfg = Config()
