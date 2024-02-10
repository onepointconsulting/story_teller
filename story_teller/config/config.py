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
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")
    assert openai_model is not None
    openai_timeout = float(os.getenv("OPENAI_TIMEOUT", 30.0))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE") == "true"
    streaming = os.getenv("OPENAI_STREAMING", "false") == "true"
    openai_temperature = float(os.getenv("OPENAI_TEMPERATURE"))
    openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))

    stories_path = Path(os.getenv("STORIES_PATH"))
    if not stories_path.exists():
        stories_path.mkdir(parents=True)

    openai_image_gen_temperature = float(os.getenv("OPENAI_IMAGE_GEN_TEMPERATURE"))

    image_model = os.getenv("IMAGE_MODEL")
    assert image_model is not None
    image_download_folder = Path(os.getenv("IMAGE_DOWNLOAD_FOLDER"))
    create_if_not_exists(image_download_folder)

    html_template_path = project_root / "templates"
    assert html_template_path.exists()

    image_intermediate_prompt = bool(os.getenv("IMAGE_INTERMEDIATE_PROMPT", "True"))

    def init_llms(self):
        openai_api_key = self.openai_api_key
        if openai_api_key is not None and len(openai_api_key) > 0:
            self.llm = ChatOpenAI(
                openai_api_key=openai_api_key,
                model=self.openai_model,
                temperature=self.openai_temperature,
                request_timeout=self.openai_timeout,
                cache=self.has_langchain_cache,
                streaming=self.streaming,
                max_tokens=self.openai_max_tokens,
            )
            self.image_llm = OpenAI(
                openai_api_key=openai_api_key,
                temperature=self.openai_image_gen_temperature,
            )


cfg = Config()
cfg.init_llms()
