from crewai import Agent, Task, Crew, Process

from story_teller.config.config import cfg
from story_teller.lib.callbacks import LLMCallbackHandler
from story_teller.model.novel_content import NovelContent
from story_teller.tools.image_dall_e_tool import image_tool
from story_teller.tools.chapter_extractor import chapter_tool
from story_teller.model.chapter_info import Chapter


llm_callback_handler = LLMCallbackHandler(name="LLM Handler")
cfg.llm.callbacks = [llm_callback_handler]


def create_writer():
    writer = Agent(
        role="Writer",
        goal="Write a novel in British English based on the chapters provided to you.",
        backstory="A talented writer who writes novels in different styles, including Tolkien or depending on the topic George Orwell.",
        allow_delegation=False,
        verbose=True,
        llm=cfg.llm,
    )
    return writer


def create_chapter_writer():
    writer = Agent(
        role="ChapterWriter",
        goal="Write a chapter for the novel",
        backstory="A talented writer who writes a chapter for the novel at a time in different styles, including Tolkien or depending on the topic George Orwell.",
        verbose=True,
        llm=cfg.llm,
    )
    return writer


def chapter_writer():
    # Define the agents
    writer = Agent(
        role="ChapterWriter",
        goal="Write an enumeration with the chapters of a story",
        backstory="Creates the skeleton of a story by getting the input and defining its chapters",
        allow_delegation=False,
        verbose=True,
        llm=cfg.llm,
    )
    return writer


def chapter_extractor():
    # Define the agents
    writer = Agent(
        role="ChapterExtractor",
        goal="Extract all of the chapters in JSON format",
        backstory="Extract all chapters in JSON format, so that we can loop through them",
        verbose=True,
        llm=cfg.llm,
    )
    return writer


reviewer = Agent(
    role="Reviewer",
    goal="Reviews the text written by the writer and sends it back to the writer in case the passages need to be re-written",
    backstory="Looks at flaws in the novels written by the writer. This role is excellent at giving feedback.",
    verbose=True,
    llm=cfg.llm,
)

graphical_artist = Agent(
    role="Graphical Artist",
    goal="Converts certain scenes to images, if they contain imagery.",
    backstory="A gifted image creators which loves both futuristic and also retro scenes",
    verbose=True,
    llm=cfg.llm,
)


def create_writer_task():
    agent = create_writer()
    task = Task(
        description="Take the chapters and expand them into a proper tale.",
        agent=agent,
    )
    return task, agent


def chapter_writer_task(novel_content: NovelContent):
    agent = chapter_writer()
    task = Task(
        description=novel_content.create_novel_prompt(),
        agent=agent,
    )
    return task, agent


def create_chapter_extractor_task():
    agent = chapter_extractor()
    task = Task(
        description="Extract all chapters that were generated in JSON format",
        agent=agent,
        tools=[chapter_tool],
    )
    return task, agent


def create_chapter_developer():
    agent = create_chapter_writer()
    task = Task(
        description="Develop a chapter in the novel", agent=agent, tools=[chapter_tool]
    )
    return task, agent


def create_chapter_crew(novel_content: NovelContent, chapter: Chapter):
    # Instantiate the crew
    task_chapter_writer, agent_chapter_writer = chapter_writer_task(novel_content)
    task_chapter_extractor, agent_chapter_extractor = create_chapter_extractor_task()
    crew = Crew(
        agents=[agent_chapter_writer, agent_chapter_extractor],
        tasks=[task_chapter_writer, task_chapter_extractor],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def create_chapter_development(novel_content: NovelContent, chapter: Chapter):
    pass
