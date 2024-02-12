import time

from typing import Union, List

from story_teller.mymidjourney.imagine import imagine_request
from story_teller.mymidjourney.message import message_request
from story_teller.mymidjourney.button import button_request
from story_teller.mymidjourney.model.message_result import MessageResult
from story_teller.mymidjourney.model.error import Error, ImageGenerationError, Stage
from story_teller.mymidjourney.config import midjourney_cfg
from story_teller.mymidjourney.log_factory import logger
from story_teller.mymidjourney.utils.download_folder import download_image


def process_image_generation(
    prompt: str, image_limit: int, upscale=True, versions=0
) -> Union[List[str], Error]:
    if upscale:
        versions = 0
    imagine_result = imagine_request(prompt)
    if type(imagine_result) == Error:
        return ImageGenerationError(
            error_code=imagine_result.error_code,
            error_message=imagine_result.error_message,
            stage=Stage.IMAGINE,
        )
    message_id = imagine_result.message_id
    # Results are either image urls (upscale == True) or message ids (upscale == False)
    results = extract_images(message_id, image_limit if upscale else versions, upscale)
    if type(results) == Error:
        return results
    if upscale:
        return results
    else:
        image_urls = []
        for message_id in results:
            upscale_results = extract_images(message_id, image_limit, True)
            if type(upscale_results) == Error:
                return upscale_results
            image_urls.extend(upscale_results)
        return image_urls


def extract_images(
    message_id: str, iterations: int, upscale=True
) -> Union[List[str], Error]:
    logger.info("Generated message id: %s", message_id)
    message_result = extract_message_result(message_id, Stage.MESSAGE_1)
    if type(message_result) == ImageGenerationError:
        return message_result
    result_list = []
    max_tries = 20
    logger.info("All buttons: %s", message_result.buttons)
    for i in range(max_tries):
        button = message_result.buttons[i]
        if button.startswith("U" if upscale else "V"):
            logger.info("Activating button: %s", button)
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
            if upscale:
                result_list.append(button_message_result.uri)
            else:
                result_list.append(button_message_result.message_id)
            if len(result_list) >= iterations:
                break
        else:
            logger.info("Ignored button: %s", button)
    return result_list


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
        logger.info("Message result progress: %s", message_result.progress)
        if message_result.progress != 100:
            time.sleep(midjourney_cfg.sleep_time)
        else:
            return message_result
    return ImageGenerationError(
        error_code=-1,
        error_message="Image generation timed out",
        stage=stage,
    )


def download_batch(image_urls: Union[List[str], Error]):
    for image_url in image_urls:
        try:
            download_image(image_url, midjourney_cfg.temp_dir)
        except:
            logger.exception("Could not download image")


if __name__ == "__main__":
    from story_teller.mymidjourney.config import midjourney_cfg

    prompt = "Please draw a picture of a beautiful deity on top of a hill in a beautiful scenery. The deity's face is full of peace."
    prompt = "Please draw the picture of a saint in a temple somewhere in India."

    def four_images():
        prompt = "Please draw a picture of a beautiful angel, who is blessing the world, surrounded by divine light. Use Leonardo da Vinci's style"
        image_urls = process_image_generation(prompt, 4, upscale=True)
        if type(image_urls) == ImageGenerationError:
            print(image_urls)
        else:
            download_batch(image_urls)

    def two_version_4_images():
        prompt = "Please draw a picture of a beautiful archangel displaying all the power and might of God"
        image_urls = process_image_generation(prompt, 4, upscale=False, versions=2)
        if type(image_urls) == ImageGenerationError:
            print(image_urls)
        else:
            download_batch(image_urls)

    four_images()
