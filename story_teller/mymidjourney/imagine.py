import json
from typing import Union, Any

import requests

from story_teller.mymidjourney.model.error import Error
from story_teller.mymidjourney.model.imagine_result import ImagineResult
from story_teller.mymidjourney.common import (
    header_factory,
    END_POINT_BASE,
    handle_error,
)
from story_teller.mymidjourney.model.imagine_result import convert_from_str


def imagine_request(prompt: str) -> Union[ImagineResult, Error]:
    data = {"prompt": prompt}
    headers = header_factory()
    return process_response(data, headers, f"{END_POINT_BASE}/imagine")


def process_response(data, headers, url):
    response = requests.post(url, data=data, headers=headers)

    def success_func(response: requests.models.Response):
        response_obj = json.loads(response.text)
        if response_obj["success"] == True:
            return convert_from_str(response.text)
        else:
            return Error(error_code=response.status_code, error_message=response.text)

    return handle_error(response, success_func)


if __name__ == "__main__":
    imagine_result = imagine_request(
        "Can you please picture of an ancient idol in a lost Hindu temple"
    )
    # '{"success":true,"messageId":"391cc79e-24e8-4818-9f62-9416bafab7f4","createdAt":"2024-02-10T20:42:13+00:00"}'
    # ImagineResult(success=True, message_id='ab29cb7f-47af-4957-afec-3ca793fd2fa4', created_at=datetime.datetime(2024, 2, 11, 13, 5, 59, tzinfo=datetime.timezone.utc))
    # ImagineResult(success=True, message_id='148d03f2-98fa-4556-863c-d2fe2d4965cf', created_at=datetime.datetime(2024, 2, 11, 13, 10, 3, tzinfo=datetime.timezone.utc))
    # ImagineResult(success=True, message_id='a425381e-6782-4456-97c2-c122c3783e95', created_at=datetime.datetime(2024, 2, 11, 13, 38, 28, tzinfo=datetime.timezone.utc))
    if type(imagine_result) == Error:
        print(f"Error: {imagine_result}")
    else:
        print(f"Success: {imagine_result}")
