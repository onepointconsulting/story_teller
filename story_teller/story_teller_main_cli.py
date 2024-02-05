import json

from datetime import datetime
from pathlib import Path
from story_teller.service.story_teller_crew import (
    llm_callback_handler,
    create_chapter_crew,
)
from story_teller.config.config import cfg
from story_teller.test.provider.novel_content_provider import (
    create_simple_novel_content,
)


def write_crew_reasonings(prefix: str, result: str):
    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    story_path = Path(cfg.stories_path / f"{prefix}_{now_str}.txt")
    with open(story_path, "w", encoding="utf-8") as f:
        for response in llm_callback_handler.responses:
            f.write(response)
            f.write("\n-----------------------------------\n")
        f.write("Result:\n")
        f.write("=======\n\n")
        f.write(result)


if __name__ == "__main__":
    # Kick off the crew's story
    crew = create_chapter_crew(create_simple_novel_content())
    result = crew.kickoff()
    # write_crew_reasonings("chapters", result)
    result_dict = json.loads(result)
