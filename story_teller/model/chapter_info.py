from typing import List, Union
from pathlib import Path
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


class DevelopedChapter(Chapter):
    content: str = Field(..., description="The content of the chapter")
    image_location: Union[Path, None] = Field(
        default=None, description="The location of the image"
    )

    def markdown(self):
        image_str = (
            f"""![{self.name}]({self.image_location.name} "{self.name}")"""
            if self.image_location is not None
            else ""
        )
        return f"""### {self.name}
#### {self.description}

{image_str}
{self.content}
"""

    def image_str(self) -> str:
        return f"""{self.name}

{self.description}
"""


class ChapterList(BaseModel):
    chapters: List[Chapter] = Field(..., description="The list of chapters")

    def __str__(self):
        out = ""
        for c in self.chapters:
            out += f"{c}\n\n"
        return out


class DevelopedChapterList(BaseModel):
    chapters: List[DevelopedChapter] = Field(
        ..., description="The list of chapters with content"
    )


class NovelResult(BaseModel):
    chapters: DevelopedChapterList = Field(
        ..., description="all of the chapters of the novel"
    )
    markdown_file: Path = Field(
        ..., description="Markdown file with the novel chapters"
    )
    html_file: Path = Field(..., description="HTML file with the novel chapters")
