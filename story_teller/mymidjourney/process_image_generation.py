import time

from typing import Union, List

from pathlib import Path

from story_teller.mymidjourney.imagine import imagine_request
from story_teller.mymidjourney.message import message_request
from story_teller.mymidjourney.button import button_request
from story_teller.mymidjourney.model.message_result import MessageResult
from story_teller.mymidjourney.model.error import Error, ImageGenerationError, Stage
from story_teller.mymidjourney.config import midjourney_cfg


MAX_BUTTONS = 4


def process_image_generation(prompt: str, image_count: int) -> Union[List[str], Error]:
    imagine_result = imagine_request(prompt)
    if type(imagine_result) == Error:
        return ImageGenerationError(
            error_code=imagine_result.error_code,
            error_message=imagine_result.error_message,
            stage=Stage.IMAGINE,
        )
    message_id = imagine_result.message_id
    message_result = extract_message_result(message_id, Stage.MESSAGE_1)
    image_urls = []
    for i in range(image_count):
        if i >= MAX_BUTTONS:
            break
        button = message_result.buttons[i]
        button_result = button_request(message_result.message_id, button)
        if type(button_result) == Error:
            return ImageGenerationError(
                error_code=button_result.error_code,
                error_message=button_result.error_message,
                stage=Stage.BUTTON,
            )
        button_message_id = button_result.message_id
        button_message_result = extract_message_result(
            button_message_id, Stage.MESSAGE_FINAL
        )
        if type(message_result) == Error:
            return ImageGenerationError(
                error_code=button_message_result.error_code,
                error_message=button_message_result.error_message,
                stage=Stage.BUTTON,
            )
        image_urls.append(button_message_result.uri)
    return image_urls


def extract_message_result(
    message_id: str, stage: str
) -> Union[MessageResult, ImageGenerationError]:
    message_result = None
    for _ in range(midjourney_cfg.message_attempts):
        message_result = message_request(message_id)
        if type(message_result) == Error:
            return ImageGenerationError(
                error_code=message_result.error_code,
                error_message=message_result.error_message,
                stage=stage,
            )
        if message_result.progress != 100:
            time.sleep(midjourney_cfg.sleep_time)
        else:
            break
    return message_result


if __name__ == "__main__":
    prompt = "Please draw a picture of a beautiful angle blessing the world surrounded by divine light"
    image_urls = process_image_generation(prompt, 4)
    for image_url in image_urls:
        print(image_url)
