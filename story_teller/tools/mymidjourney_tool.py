from typing import Union
from pathlib import Path

from story_teller.config.config import cfg
from story_teller.mymidjourney.process_image_generation import process_image_generation
from story_teller.mymidjourney.model.error import ImageGenerationError
from story_teller.model.developed_chapter import DevelopedChapter
from story_teller.mymidjourney.utils.download_folder import download_image
from story_teller.test.provider.chapter_content_provider import create_developed_chapter


def generate_image(developed_chapter: DevelopedChapter) -> Union[Path, None]:
    image_urls = process_image_generation(
        developed_chapter.name_description_with_style(), 1, upscale=True
    )
    if type(image_urls) == ImageGenerationError or len(image_urls) == 0:
        return None
    return download_image(image_urls[0], cfg.image_download_folder)


if __name__ == "__main__":
    developed_chapter = create_developed_chapter()
    image_path = generate_image(developed_chapter)
    print(image_path)
