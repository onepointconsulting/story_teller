import unittest

from story_teller.mymidjourney.model.message_result import convert_from_str


class TestMessageResult(unittest.TestCase):
    def test_convert_from_str(self):
        message = """
{
    "prompt": "Can you please picture a beautiful angel sending blessings to the world",
    "uri": "https://cdn.discordapp.com/attachments/1184835720645460041/1205977239561437294/sabelisam_Can_you_please_picture_a_beautiful_angel_sending_bles_ee7b1577-6766-45fe-89c6-6493f32dc6fd.png?ex=65da54d3&is=65c7dfd3&hm=d0f87425d6bc647f88235c48eeeee21629413bb535aa8eb0e23dc6d54ee6c7ed&",
    "progress": 100,
    "buttons": [
        "U1",
        "U2",
        "U3",
        "U4",
        "🔄",
        "V1",
        "V2",
        "V3",
        "V4"
    ],
    "messageId": "391cc79e-24e8-4818-9f62-9416bafab7f4",
    "createdAt": "2024-02-10T20:42:13+00:00",
    "updatedAt": "2024-02-10T20:43:00+00:00"
}"""
        message_result = convert_from_str(message)
        assert message_result.created_at is not None
        assert message_result.updated_at is not None


if __name__ == "__main__":
    unittest.main()
