import requests
import os

from pathlib import Path

from typing import Union
from story_teller.config.config import cfg
from story_teller.config.log_factory import logger
from story_teller.config.toml_support import prompts

from langchain.chains import LLMChain
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from story_teller.model.developed_chapter import DevelopedChapter
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from story_teller.mymidjourney.utils.download_folder import download_image


def generate_image(developed_chapter: DevelopedChapter) -> Union[Path, None]:
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template=prompts["story"]["image_generation"]["prompt_template"],
    )

    os.environ["OPENAI_API_KEY"] = cfg.openai_api_key
    logger.info("Using Dall-E quality: %s", cfg.image_quality_dall_e)
    dall_e = DallEAPIWrapper(quality=cfg.image_quality_dall_e)
    dall_e.model_name = cfg.image_model

    if cfg.image_intermediate_prompt:
        logger.info("Using intermediate prompt for image generation")
        chain = LLMChain(llm=cfg.image_llm, prompt=prompt)
        invocation = chain.invoke(developed_chapter.image_str())
        invocation_text = invocation.get("text")
        if invocation_text is None:
            return None
        image_style_remark = prompts["story"]["image_generation"]["image_style_remark"]
        invocation_text = f"""{invocation_text}

    {image_style_remark}
        """
        image_url = dall_e.run(invocation_text)
    else:
        logger.info("Using no intermediate prompt to generate images")
        image_url = dall_e.run(developed_chapter.name_description_with_style())
    return download_image(image_url, cfg.image_download_folder)


image_tool = Tool(
    name="Image tool",
    func=generate_image,
    description="useful for image generation from prompts",
)

if __name__ == "__main__":
    cfg.image_intermediate_prompt = True
    generated_image = image_tool.invoke("A beautiful castle on top of a hill at sunset")
    print(generated_image)
