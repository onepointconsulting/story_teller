import unittest
import json

from story_teller.tools.image_dall_e_tool import extract_image_path


class TestImageDallETool(unittest.TestCase):
    def test_extract_image_path(self):
        image = "img-9U349cyy3YXVmZhegXUMZgxm.png"
        sample_path = f"https://oaidalleapiprodscus.blob.core.windows.net/private/org-uCh4BCLezybIYgdbRbsPUjgk/user-x08zNprdtJfrWhPBAJ6q7OAA/{image}?st=2024-01-19T13%3A52%3A04Z&se=2024-01-19T15%3A52%3A04Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-18T17%3A25%3A47Z&ske=2024-01-19T17%3A25%3A47Z&sks=b&skv=2021-08-06&sig=M3WTK6yI/o5a2wAwHqPx2EqJXZUaDK7CFWQ9q75vDN8%3D"
        image_extracted = extract_image_path(sample_path)
        assert image_extracted == image

    def test_extract_image_path_2(self):
        sample_path = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-uCh4BCLezybIYgdbRbsPUjgk/user-x08zNprdtJfrWhPBAJ6q7OAA/img-1rYHzstKpAST2zpsPm5F2oYI.png?st=2024-01-19T14%3A56%3A57Z&se=2024-01-19T16%3A56%3A57Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-19T11%3A42%3A44Z&ske=2024-01-20T11%3A42%3A44Z&sks=b&skv=2021-08-06&sig=%2BmWPyAlxZbejwvPXKCNcX1Xr/lkClO80ov8aMiCy%2BDs%3D"
        image_extracted = extract_image_path(sample_path)
        assert image_extracted == "img-1rYHzstKpAST2zpsPm5F2oYI.png"


if __name__ == "__main__":
    unittest.main()
