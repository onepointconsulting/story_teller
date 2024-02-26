from datetime import datetime

from typing import List, Union, Callable, Any
from pathlib import Path
import shutil

from langchain.chains import create_extraction_chain_pydantic, LLMChain
from langchain.prompts import (
    PromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from story_teller.config.config import cfg
from story_teller.config.toml_support import prompts
from story_teller.model.novel_content import NovelContent, ChapterDevelopment
from story_teller.model.developed_chapter import (
    DevelopedChapter,
    DevelopedChapterList,
    NovelResult,
)
from story_teller.model.chapter_info import (
    ChapterList,
    Chapter,
)
from story_teller.tools.image_dall_e_tool import generate_image
from story_teller.config.log_factory import logger
from story_teller.service.markdown_conversion import convert_markdown_html
from story_teller.service.cleanup_service import cleanup, comment_cleanup
from story_teller.service.story_callback import StoryCallbackMixin
import story_teller.tools.mymidjourney_tool as mymidjourney_tool
from story_teller.mymidjourney.config import midjourney_cfg
from story_teller.service.pdf_service import convert_to_pdf


def extract_entity(
    res: List[dict],
) -> Union[Union[ChapterList, DevelopedChapterList], None]:
    if len(res["text"]) > 0:
        return res["text"][0]
    return None


def create_chapters(novel_content: NovelContent) -> ChapterList:
    messages = []
    messages.append(
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["novel_content"],
                template=prompts["chapters"]["human_message"],
            )
        )
    )
    append_style_message(novel_content, messages)
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = create_extraction_chain_pydantic(
        pydantic_schema=ChapterList, llm=cfg.llm, prompt=prompt, verbose=True
    )
    style_info = novel_content.style_info
    res = chain.invoke(
        {
            "novel_content": novel_content.create_novel_prompt(),
            "author": style_info.author,
            "book": style_info.book,
        }
    )
    return extract_entity(res)


def append_style_message(
    novel_content: NovelContent, messages: List[HumanMessagePromptTemplate]
):
    if novel_content.style_info is not None:
        messages.append(
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["author", "book"],
                    template=prompts["chapters"]["style_message"],
                )
            )
        )


def develop_chapter(chapter_development: ChapterDevelopment) -> str:
    messages = []
    messages.append(
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[
                    "novel_content",
                    "chapter_sequence",
                    "chapter_name",
                    "chapter_description",
                    "all_chapters",
                ],
                template=prompts["story"]["develop_chapter"]["prompt_template"],
            )
        )
    )

    novel_content: NovelContent = chapter_development.novel_content
    chapter_list: ChapterList = chapter_development.chapter_list
    chapter: Chapter = chapter_development.chapter
    append_style_message(novel_content, messages)
    prompt = ChatPromptTemplate(messages=messages)
    chain = LLMChain(llm=cfg.llm, prompt=prompt, verbose=True)
    style_info = novel_content.style_info
    res = chain.invoke(
        {
            "novel_content": novel_content.create_novel_prompt(),
            "chapter_sequence": chapter.sequence,
            "chapter_name": chapter.name,
            "chapter_description": chapter.description,
            "all_chapters": str(chapter_list),
            "author": style_info.author,
            "book": style_info.book,
        }
    )
    return res["text"]


def retry_func(func: Callable, times: int) -> Any:
    for _ in range(times):
        try:
            return func()
        except:
            logger.exception("Failed to process in try. Retrying ...")
    raise Exception(f"Could not execute {func}")


def develop_story(
    novel_content: NovelContent,
    story_callback: StoryCallbackMixin,
    cleanup_text: bool = True,
) -> NovelResult:
    story_path = create_story_path_folder()
    story_path.mkdir(parents=True)

    write_main_titles(novel_content, story_path)

    res = create_chapters(novel_content)
    chapter_list = res.chapters
    story_callback.on_chapters_generated([c.name for c in res.chapters])
    developer_chapter_list = DevelopedChapterList(chapters=[])
    for i, chapter in enumerate(chapter_list):
        chapter_development = ChapterDevelopment(
            novel_content=novel_content,
            chapter_list=ChapterList(chapters=chapter_list),
            chapter=chapter,
        )

        def process_develop_chapter():
            return develop_chapter(chapter_development)

        content = retry_func(process_develop_chapter, 3)
        content = cleanup(content)
        logger.info(content)
        developed_chapter = DevelopedChapter(
            sequence=chapter.sequence,
            name=chapter.name,
            description=chapter.description,
            content=content,
            novel_content=novel_content,
        )
        developed_chapter.image_location = generate_image_from_chapter(
            developed_chapter
        )
        markdown_file = story_path / "novel.md"

        # Clean up
        if cleanup_text:
            story_callback.on_chapter_cleanup(developed_chapter.name)
            developed_chapter.content = comment_cleanup(developed_chapter)

        with open(markdown_file, "a", encoding="utf-8") as nf:
            if developed_chapter.image_location is not None:
                if developed_chapter.image_location.exists():
                    image_location = story_path / developed_chapter.image_location.name
                    shutil.move(developed_chapter.image_location, image_location)
                    developed_chapter.image_location = image_location
            nf.write(f"{developed_chapter.markdown()}\n\n")

        developer_chapter_list.chapters.append(developed_chapter)
        story_callback.on_chapter_finish(
            developed_chapter.name, i + 1, len(chapter_list)
        )

    generated_html_file = convert_markdown_html(
        story_title=novel_content.title,
        markdown_file=markdown_file,
        target_parent=story_path,
    )
    story_callback.on_html_finished(generated_html_file)
    logger.info(f"Generated html file: {generated_html_file}")
    return NovelResult(
        chapters=developer_chapter_list,
        markdown_file=markdown_file,
        html_file=generated_html_file,
        pdf_file=convert_to_pdf(generated_html_file),
    )


def write_main_titles(novel_content: NovelContent, story_path: Path):
    with open(story_path / "novel.md", "w", encoding="utf-8") as nf:
        nf.write(f"# {novel_content.title}\n\n")
        nf.write(f"## {novel_content.subtitle}\n\n")
        nf.write(f"### Synopsis\n\n")
        nf.write(f"{novel_content.details}\n\n")
        style_info = novel_content.style_info
        if style_info is not None:
            nf.write(f"\n#### Based on {style_info.book} by {style_info.author}\n\n")
            nf.write(
                f"\n#### Texts generated by {cfg.openai_model}, images generated by {'Midjourney' if cfg.use_midjourney else 'Dall-E'}\n\n"
            )


def create_story_path_folder():
    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")

    story_path = cfg.stories_path / f"novel_{now_str}"
    return story_path


def generate_image_from_chapter(
    developed_chapter: DevelopedChapter,
) -> Union[Path, None]:
    try:
        if cfg.use_midjourney and midjourney_cfg.bearer_token is not None:
            return mymidjourney_tool.generate_image(developed_chapter)
        return generate_image(developed_chapter)
    except:
        logger.exception("Could not generate image")
        return None


if __name__ == "__main__":
    from story_teller.test.provider.novel_content_provider import (
        create_simple_novel_content,
        create_simple_novel_content_2,
        create_simple_novel_content_3,
    )

    class SimpleStoryCallback(StoryCallbackMixin):
        def on_chapter_finish(
            self, chapter_name: str, completed: int, missing: int
        ) -> Any:
            logger.info("Finished %s - %d out of %d", chapter_name, completed, missing)

    novel_content = create_simple_novel_content_3()
    novel_result = develop_story(novel_content, SimpleStoryCallback())
