import unittest
import json

from story_teller.config.config import cfg
from story_teller.service.markdown_conversion import convert_markdown_html
from story_teller.test.provider.novel_content_provider import (
    create_simple_novel_content_2,
)


class TestMarkdownConversion(unittest.TestCase):
    def test_topic(self):
        novel_content = create_simple_novel_content_2()
        title = novel_content.title
        assert title is not None
        novel_folder = cfg.project_root / "samples/novel_20240123_100327"
        assert novel_folder is not None
        markdown_file = novel_folder / "novel.md"
        novel_html = convert_markdown_html(
            story_title=title, markdown_file=markdown_file, target_parent=novel_folder
        )
        assert novel_html.exists()


if __name__ == "__main__":
    unittest.main()
