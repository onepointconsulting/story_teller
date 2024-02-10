from typing import List

from pydantic.v1 import BaseModel, Field


class Chapter(BaseModel):
    sequence: int = Field(..., description="The number of the chapter in the sequence")
    name: str = Field(..., description="The chapter name")
    description: str = Field(..., description="The chapter description")

    def __str__(self):
        return f"""{self.sequence}. {self.name}
description: {self.description}
"""

    def __repr__(self) -> str:
        return self.__str__()


class ChapterList(BaseModel):
    chapters: List[Chapter] = Field(..., description="The list of chapters")

    def __str__(self):
        out = ""
        for c in self.chapters:
            out += f"{c}\n\n"
        return out
