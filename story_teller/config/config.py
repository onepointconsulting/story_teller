import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI

load_dotenv()


def create_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


class Config:
    project_root = Path(os.getenv("PROJECT_ROOT", os.getcwd()))

    # OpenAI related
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL")
    assert openai_model is not None
    openai_timeout = float(os.getenv("OPENAI_TIMEOUT", 30.0))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE") == "true"
    streaming = os.getenv("OPENAI_STREAMING") == "true"
    openai_temperature = float(os.getenv("OPENAI_TEMPERATURE"))
    openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model=openai_model,
        temperature=openai_temperature,
        request_timeout=openai_timeout,
        cache=has_langchain_cache,
        streaming=streaming,
        max_tokens=openai_max_tokens,
    )
    stories_path = Path(os.getenv("STORIES_PATH"))
    if not stories_path.exists():
        stories_path.mkdir(parents=True)

    openai_image_gen_temperature = float(os.getenv("OPENAI_IMAGE_GEN_TEMPERATURE"))
    image_llm = OpenAI(
        openai_api_key=openai_api_key, temperature=openai_image_gen_temperature
    )
    image_model = os.getenv("IMAGE_MODEL")
    assert image_model is not None
    image_download_folder = Path(os.getenv("IMAGE_DOWNLOAD_FOLDER"))
    create_if_not_exists(image_download_folder)

    html_template_path = project_root / "templates"
    assert html_template_path.exists()


cfg = Config()
