from pathlib import Path
from typing import Union, List, Optional

from pydantic.v1 import BaseModel, Field

from story_teller.model.chapter_info import Chapter
from story_teller.model.novel_content import NovelContent


class DevelopedChapter(Chapter):
    content: str = Field(..., description="The content of the chapter")
    image_location: Union[Path, None] = Field(
        default=None, description="The location of the image"
    )
    novel_content: NovelContent

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

{self.content}
"""

    def name_description_with_style(self) -> str:
        style_info = ""
        if self.novel_content is not None and self.novel_content.style_info is not None:
            style_info = f"Inspired on `{self.novel_content.style_info.book}` by `{self.novel_content.style_info.author}`"
        return f"""{self.name}

{self.description}

{style_info}
"""


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
    pdf_file: Optional[Path] = Field(..., description="The generated PDF file")
