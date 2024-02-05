from typing import Union
from pydantic.v1 import BaseModel, Field

from story_teller.model.chapter_info import ChapterList, Chapter


class StyleInfo(BaseModel):
    author: str = Field(..., description="The author")
    book: str = Field(..., description="The book")


class NovelContent(BaseModel):
    title: str = Field(..., description="The topic of the novel")
    subtitle: str = Field(..., description="The subtitle of the novel")
    details: str = Field(..., description="The novel details")
    style_info: Union[StyleInfo, None] = Field(
        ..., description="The style information."
    )

    def create_novel_prompt(self) -> str:
        return f"""# {self.title}
## {self.subtitle}

{self.details}
    """


def create_empty_novel_content() -> NovelContent:
    style_info = StyleInfo(author="Tolkien", book="Lord of the Rings")
    return NovelContent(title="", subtitle="", details="", style_info=style_info)


class ChapterDevelopment(BaseModel):
    novel_content: NovelContent = Field(
        ..., description="The main content of the novel with title subtitle and details"
    )
    chapter_list: ChapterList = Field(
        ..., description="The list of pre-generated chapters"
    )
    chapter: Chapter = Field(..., description="The single chapter in a novel")
