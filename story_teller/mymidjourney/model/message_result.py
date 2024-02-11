import json
from typing import List, Optional

from dataclasses import dataclass
from datetime import datetime


@dataclass
class MessageResult:
    prompt: str
    uri: Optional[str]
    progress: Optional[int]
    buttons: Optional[List[str]]
    message_id: str
    created_at: datetime
    updated_at: datetime


def convert_from_str(json_str: str):
    res_obj = json.loads(json_str)
    created_at = datetime.fromisoformat(res_obj["createdAt"])
    updated_at = datetime.fromisoformat(res_obj["updatedAt"])
    return MessageResult(
        prompt=res_obj["prompt"],
        uri=res_obj.get("uri"),
        progress=res_obj.get("progress"),
        buttons=res_obj.get("buttons"),
        message_id=res_obj["messageId"],
        created_at=created_at,
        updated_at=updated_at,
    )
