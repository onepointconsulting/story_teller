import unittest

from story_teller.service.cleanup_service import cleanup


class TestCleanup(unittest.TestCase):
    def test_extract_image_path(self):
        sample_txt = """=== START CHAPTER ===
2. The Storm of Fates

In the waning light of a day that had begun with no portents of sorrow, Calypso stood amidst the remnants of her once joyful hamlet. The sky had unleashed its fury without warning, a tempest so fierce it seemed a fell beast had descended upon their homes. The clouds, as if in mourning, hung low, and the rain had been as tears shed by the very heavens, lamenting the devastation wrought below.
=== END CHAPTER ===
"""
        res_txt = cleanup(sample_txt)
        assert res_txt is not None
        assert "=== START CHAPTER ===" not in res_txt
        print(res_txt)


if __name__ == "__main__":
    unittest.main()
