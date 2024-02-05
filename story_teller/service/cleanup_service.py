import re

from story_teller.config.toml_support import prompts
from story_teller.config.config import cfg
from story_teller.model.chapter_info import DevelopedChapter

from langchain.chains import LLMChain
from langchain.prompts import (
    PromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.prompts import (
    PromptTemplate,
    HumanMessagePromptTemplate,
)


class CleanupParams:
    CHAPTER_NAME = "chapter_name"
    CHAPTER = "chapter"


def cleanup(content: str):
    assert content is not None
    return re.sub(r"===[^=]+===", "\n", content)


def prepare_prompt():
    messages = []
    messages.append(
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[
                    CleanupParams.CHAPTER_NAME,
                    CleanupParams.CHAPTER,
                ],
                template=prompts["story"]["cleanup_chapter"]["prompt_template"],
            )
        )
    )
    return ChatPromptTemplate(messages=messages)


def comment_cleanup(chapter: DevelopedChapter) -> str:
    prompt = prepare_prompt()
    chain = LLMChain(llm=cfg.llm, prompt=prompt, verbose=True)
    res = chain.invoke(
        {
            CleanupParams.CHAPTER_NAME: chapter.name,
            CleanupParams.CHAPTER: chapter.content,
        }
    )
    return res["text"]


if __name__ == "__main__":
    from story_teller.test.provider.chapter_content_provider import (
        create_developed_chapter,
    )

    chapter = create_developed_chapter()
    res = comment_cleanup(chapter)
    print(type(res))
    print(res)
