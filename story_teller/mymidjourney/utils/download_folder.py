from pathlib import Path

from typing import Union

import requests

from story_teller.mymidjourney.log_factory import logger


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
        logger.info(f"Image successfully downloaded to folder {full_path}")
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
