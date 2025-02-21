import os
import re
import asyncio
import logging
from playwright.async_api import async_playwright, TimeoutError

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)[:100]


async def scrape_medium_article(article_url: str) -> str:
    """Scrapes a Medium article and takes a screenshot."""
    os.makedirs("screenshots", exist_ok=True)
    screenshot_path = None  # Default None if screenshot fails

    try:
        async with async_playwright() as pw:
            logging.info(f"Launching Playwright to scrape: {article_url}")
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1280, "height": 800})

            await page.goto("http://readmedium.com", timeout=60000)
            await page.fill("input[placeholder='Medium Article URL']", article_url)
            await page.locator("button:text('GO')").click()
            await page.wait_for_load_state("networkidle")

            # Hide navbar for cleaner screenshot
            await page.add_style_tag(content="nav { display: none !important; }")

            article_tag = await page.query_selector("article")
            if article_tag:
                article_title = await page.title()
                screenshot_path = f"screenshots/{sanitize_filename(article_title)}.png"
                await article_tag.screenshot(path=screenshot_path)
                logging.info(f"Screenshot saved as {screenshot_path}")
            else:
                logging.error(
                    "❌ Article content not found. Screenshot not taken.")

            await browser.close()

    except TimeoutError:
        logging.error("❌ Timeout while loading the page.")
    except Exception as e:
        logging.error(f"❌ An error occurred: {e}")

    return screenshot_path


if __name__ == "__main__":
    article_url = input("Enter the URL of the article you want to scrape: ")
    screenshot_path = asyncio.run(scrape_medium_article(article_url))
    print(
        f"Screenshot path: {screenshot_path if screenshot_path else 'Failed to capture screenshot.'}")
