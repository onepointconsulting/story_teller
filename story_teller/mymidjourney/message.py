from typing import Union

import requests

from story_teller.mymidjourney.common import (
    header_factory,
    END_POINT_BASE,
    handle_error,
)
from story_teller.mymidjourney.model.message_result import (
    MessageResult,
    convert_from_str,
)
from story_teller.mymidjourney.model.error import Error


def message_request(message_id: str) -> Union[MessageResult, Error]:
    headers = header_factory()
    response = requests.get(f"{END_POINT_BASE}/message/{message_id}", headers=headers)

    def success_func(response: requests.models.Response):
        return convert_from_str(response.text)

    return handle_error(response, success_func)


if __name__ == "__main__":
    # message_id = "ab29cb7f-47af-4957-afec-3ca793fd2fa4"
    # message_id = "148d03f2-98fa-4556-863c-d2fe2d4965cf"
    # message_id = "391cc79e-24e8-4818-9f62-9416bafab7f4"
    message_id = "7b2486d3-8eb2-4dcf-a707-16af90a72140"
    message_result = message_request(message_id)
    print(message_result)
