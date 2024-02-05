from typing import Any


class StoryCallbackMixin:
    """Mixin for story callbacks."""

    def on_chapter_finish(self, chapter_name: str, completed: int, total: int) -> Any:
        """Run on new LLM token. Only available when streaming is enabled.

        Args:
            chapter_name (str): The chapter that was generated
            completed (int): How many chapters were finished.
            missing (int): How many chapters are missing.
        """

    def on_chapter_cleanup(self, chapter_name: str) -> Any:
        """Run when the chapter is being cleaned up..

        Args:
            chapter_name (str): The chapter that was generated
        """
