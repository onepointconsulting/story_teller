from typing import Union, Any, Callable

import requests

from story_teller.mymidjourney.config import midjourney_cfg
from story_teller.mymidjourney.model.error import Error

END_POINT_BASE = "https://api.mymidjourney.ai/api/v1/midjourney"


def header_factory() -> dict:
    return {"Authorization": f"Bearer {midjourney_cfg.bearer_token}"}


def handle_error(
    response: requests.models.Response, success_func: Callable
) -> Union[Any, EOFError]:
    if response.status_code >= 200 and response.status_code < 300:
        return success_func(response)
    else:
        return Error(error_code=response.status_code, error_message=response.text)
