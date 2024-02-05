import requests
from pathlib import Path

from typing import Union
from story_teller.config.config import cfg
from story_teller.config.log_factory import logger
from story_teller.config.toml_support import prompts

from langchain.chains import LLMChain
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper


def generate_image(text: str) -> Union[Path, None]:
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template=prompts["story"]["image_generation"]["prompt_template"],
    )
    chain = LLMChain(llm=cfg.image_llm, prompt=prompt)
    dall_e = DallEAPIWrapper()
    dall_e.model_name = cfg.image_model
    invocation = chain.invoke(text)
    invocation_text = invocation.get("text")
    if invocation_text is None:
        return None
    image_style_remark = prompts["story"]["image_generation"]["image_style_remark"]
    invocation_text = f"""{invocation_text}

{image_style_remark}
    """
    image_url = dall_e.run(invocation_text)
    return download_image(image_url, cfg.image_download_folder)


def download_image(image_url: str, folder_path: Path) -> Union[Path, None]:
    # Extract the image name from the URL
    image_name = extract_image_path(image_url)

    # Create the full path to save the image
    full_path = folder_path / image_name

    # Send a GET request to the image URL
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary write mode and save the image
        full_path.write_bytes(response.content)
        logger.info(f"Image successfully downloaded: {full_path}")
        return full_path
    else:
        logger.error(
            "Failed to download image with response code {response.status_code}"
        )
        return None


def extract_image_path(image_url: str) -> str:
    initial_split = image_url.split("?")
    first_chunk = initial_split[0]
    image_name = first_chunk.split("/")[-1]
    return image_name


image_tool = Tool(
    name="Image tool",
    func=generate_image,
    description="useful for image generation from prompts",
)

if __name__ == "__main__":
    generated_image = image_tool.invoke("A beautiful castle on top of a hill at sunset")
    print(generated_image)
