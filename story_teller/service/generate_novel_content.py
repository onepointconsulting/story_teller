from typing import Union

from langchain.prompts import (
    PromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from story_teller.config.config import cfg
from story_teller.config.toml_support import prompts
from story_teller.model.novel_content import NovelContent
from langchain.chains import create_extraction_chain_pydantic, LLMChain


def create_prompt():
    messages = []
    messages.append(
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],
                template=prompts["story"]["generate_novel_content"]["human_message"],
            )
        )
    )
    return ChatPromptTemplate.from_messages(messages)


def generate_novel_content() -> Union[NovelContent, None]:
    prompt = create_prompt()
    chain = create_extraction_chain_pydantic(
        pydantic_schema=NovelContent, llm=cfg.llm, prompt=prompt, verbose=True
    )
    dictionary = chain.invoke({})
    if "text" in dictionary and len(dictionary) > 0:
        return NovelContent.parse_obj(dictionary["text"][0])
    return None


if __name__ == "__main__":
    novel_content = generate_novel_content()
    print(novel_content)
    print(type(novel_content))
