from typing import Union

from langchain.chains import create_extraction_chain_pydantic
from langchain.agents import Tool

from story_teller.model.chapter_info import ChapterList
from story_teller.config.config import cfg
from story_teller.config.toml_support import prompts

chain = create_extraction_chain_pydantic(pydantic_schema=ChapterList, llm=cfg.llm)


def extract_chapters(content: str) -> ChapterList:
    human_message = prompts["chapters"]["human_message"]
    return chain.invoke(human_message.format(content=content))


def extract_chapters_json(content: str) -> Union[str, None]:
    result: dict = extract_chapters(content=content)
    chapter_list: List[ChapterList] = result.get("text")
    for chapter in chapter_list:
        return chapter.json()
    return None


chapter_tool = Tool(
    name="Chapter tool",
    func=extract_chapters_json,
    description="useful for extracting the tools in JSON format",
)


if __name__ == "__main__":
    from typing import List
    from story_teller.test.provider.chapter_content_provider import (
        create_sample_chapter_content,
    )
    from story_teller.config.log_factory import logger

    content = create_sample_chapter_content()
    result: Union[str, None] = extract_chapters_json(content)
    logger.info(result)
