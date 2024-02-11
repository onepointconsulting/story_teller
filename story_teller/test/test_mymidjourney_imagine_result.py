import unittest

from story_teller.mymidjourney.model.imagine_result import convert_from_str


class TestImagineResult(unittest.TestCase):
    def test_convert_from_str(self):
        message = """{"success":true,"messageId":"391cc79e-24e8-4818-9f62-9416bafab7f4","createdAt":"2024-02-10T20:42:13+00:00"}"""
        message_result = convert_from_str(message)
        assert message_result.created_at is not None
        assert message_result.message_id is not None
        assert message_result.success == True


if __name__ == "__main__":
    unittest.main()
