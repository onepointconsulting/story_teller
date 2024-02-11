from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Error:
    error_code: int
    error_message: str


class Stage(StrEnum):
    IMAGINE = "Imagine"
    MESSAGE_1 = "Message 1"
    BUTTON = "Button 1"
    MESSAGE_FINAL = "Message Final"


@dataclass
class ImageGenerationError(Error):
    stage: Stage
