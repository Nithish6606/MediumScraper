import os
import re
from playwright.sync_api import sync_playwright, TimeoutError


def sanitize_filename(filename: str) -> str:
    # Remove invalid characters and limit length
    return re.sub(r'[\\/*?:"<>|]', "", filename)[:100]


def scrape_medium_article(article_url: str) -> str:
    # Create screenshots directory if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto("http://readmedium.com")

            page.get_by_placeholder("Medium Article URL").fill(article_url)
            page.get_by_role("button").get_by_text("GO ").click()
            page.wait_for_load_state("networkidle")

            # Inject CSS to hide the navigation bar
            page.add_style_tag(content="nav { display: none !important; }")

            # Get the article title and use it as the screenshot name
            article_title = page.title()
            screenshot_name = f"screenshots/{sanitize_filename(article_title)}.png"

            article_tag = page.query_selector("article")
            if article_tag:
                article_tag.screenshot(path=screenshot_name)
                print(f"Screenshot saved as {screenshot_name}")
            else:
                print("Article tag not found.")
                screenshot_name = ""

            browser.close()
            return screenshot_name

    except TimeoutError:
        print("Timeout while loading the page.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


if __name__ == "__main__":
    article_url = input("Enter the URL of the article you want to scrape: ")
    screenshot_path = scrape_medium_article(article_url)
    print(f"Screenshot path: {screenshot_path}")