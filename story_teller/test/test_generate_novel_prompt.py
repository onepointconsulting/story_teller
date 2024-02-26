import unittest

from story_teller.service.generate_novel_content import create_prompt


class TestCleanup(unittest.TestCase):
    def test_generate_novel_prompt(self):
        prompt = create_prompt()
        assert prompt is not None


if __name__ == "__main__":
    unittest.main()
