from pathlib import Path

import markdown2

from story_teller.config.config import cfg


def convert_markdown_html(
    story_title: str, markdown_file: Path, target_parent: Path
) -> Path:
    assert markdown_file is not None
    assert markdown_file.exists()
    html_template = (cfg.html_template_path / "story_conversion.html").read_text()
    assert html_template is not None
    markdown_html = markdown2.markdown_path(markdown_file)
    html_end_result = html_template.replace("@story_title@", story_title).replace(
        "@full_story@", markdown_html
    )
    assert target_parent.exists()
    story_file = target_parent / "novel.html"
    story_file.write_text(html_end_result, encoding="utf-8")
    return story_file
