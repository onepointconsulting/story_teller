import unittest
import json

from story_teller.test.provider.novel_content_provider import (
    create_simple_novel_content,
)


class TestModel(unittest.TestCase):
    def test_topic(self):
        topic = create_simple_novel_content()
        json_schema = topic.schema_json()
        assert json_schema is not None
        json.dumps(json_schema)


if __name__ == "__main__":
    unittest.main()
