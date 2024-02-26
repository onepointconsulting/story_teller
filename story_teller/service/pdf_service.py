from typing import Union

from pathlib import Path

from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright

from story_teller.config.log_factory import logger


def convert_to_pdf(html_file: Path) -> Union[Path, None]:
    logger.info("Generating PDF for %s", html_file)
    output_file = html_file.parent / f"{html_file.stem}.pdf"
    try:
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                browser = browser_type.launch()
                page = browser.new_page()
                page.goto(html_file.absolute().as_uri())
                output_file = html_file.parent / f"{html_file.stem}.pdf"
                page.pdf(path=output_file)
                browser.close()
        return output_file
    except:
        logger.exception("Failed to export PDF.")
        return None


if __name__ == "__main__":
    html_file = Path(
        "/tmp/story_teller/output_2/output/novel_20240212_115453/novel.html"
    )
    pdf_file = convert_to_pdf(html_file)
    print(pdf_file)
