import os
from playwright.sync_api import sync_playwright


def scrape_medium_article(article_url: str) -> str:
    # Create screenshots directory if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True,slow_mo=4000)
    page = browser.new_page()
    page.goto("http://readmedium.com")

    page.get_by_placeholder("Medium Article URL").fill(article_url)
    page.get_by_role("button").get_by_text("GO ").click()

    # Get the article title and use it as the PDF name
    article_title = page.title()
    # Limit filename length
    pdf_name = f"screenshots/{article_title[:50]}.pdf"

    # Save the article as a PDF
    page.pdf(path=pdf_name, format="A4")

    print(f"PDF saved as {pdf_name}")
    browser.close()
    pw.stop()

    return pdf_name


if __name__ == "__main__":
    article_url = input("Enter the URL of the article you want to scrape: ")
    pdf_path = scrape_medium_article(article_url)
    print(f"PDF path: {pdf_path}")
