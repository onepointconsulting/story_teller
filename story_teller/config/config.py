import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI, OpenAI

from story_teller.config.log_factory import logger

load_dotenv(find_dotenv())


def create_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


class Config:
    project_root = Path(os.getenv("PROJECT_ROOT", os.getcwd()))

    # OpenAI related
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    logger.info("Using Open AI API Key %s", openai_api_key)
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")
    assert openai_model is not None
    openai_timeout = float(os.getenv("OPENAI_TIMEOUT", 180.0))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE", "false") == "true"
    streaming = os.getenv("OPENAI_STREAMING", "false") == "true"
    openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))

    image_model = os.getenv("IMAGE_MODEL", "dall-e-3")
    assert image_model is not None
    image_quality_dall_e = os.getenv("IMAGE_QUALITY_DALL_E", "standard")
    assert image_quality_dall_e is not None

    openai_image_gen_temperature = float(
        os.getenv("OPENAI_IMAGE_GEN_TEMPERATURE", "0.7")
    )

    tmp_folder_str = os.getenv("TMP_FOLDER", "")
    logger.info("Using stories tmp_folder_str %s", tmp_folder_str)

    html_template_path = project_root / "templates"
    assert html_template_path.exists()

    image_intermediate_prompt = bool(os.getenv("IMAGE_INTERMEDIATE_PROMPT", "True"))
    use_midjourney = os.getenv("USE_MIDJOURNEY", "false") == "true"

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
            self.init_image_llm()
            
    def init_image_llm(self):
        openai_api_key = self.openai_api_key
        self.image_llm = OpenAI(
                openai_api_key=openai_api_key,
                temperature=self.openai_image_gen_temperature,
            )

    def init_temp_folders(self):
        if self.tmp_folder_str != "":
            self.tmp_folder = Path(self.tmp_folder_str)
            self.stories_path = self.tmp_folder / "output"
            create_if_not_exists(self.stories_path)
            logger.info("Using stories path %s", self.stories_path)

            self.image_download_folder = self.tmp_folder / "image_download_folder"
            create_if_not_exists(self.image_download_folder)


cfg = Config()
cfg.init_llms()
cfg.init_temp_folders()
