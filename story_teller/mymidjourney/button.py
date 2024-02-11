from typing import Union

from story_teller.mymidjourney.model.imagine_result import ImagineResult
from story_teller.mymidjourney.model.error import Error
from story_teller.mymidjourney.common import header_factory, END_POINT_BASE
from story_teller.mymidjourney.imagine import process_response


def button_request(message_id: str, button: str) -> Union[ImagineResult, Error]:
    data = {"messageId": message_id, "button": button}
    headers = header_factory()
    return process_response(data, headers, f"{END_POINT_BASE}/button")
