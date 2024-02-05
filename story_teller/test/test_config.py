import unittest

from story_teller.config.config import cfg


class TestConfig(unittest.TestCase):
    def test_config(self):
        assert cfg is not None
        assert cfg.openai_timeout > 0.0
        # assert cfg.open_ai_client is not None


if __name__ == "__main__":
    unittest.main()
