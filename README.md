# MediumScraper

This project scrapes Medium articles and sends screenshots via a Telegram bot.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/MediumScraper.git
    cd MediumScraper
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Install Playwright browsers:

    ```sh
    playwright install
    ```

5. Install Playwright dependencies:

    ```sh
    playwright install-deps
    ```

6. Create a `.env` file in the root directory and add your environment variables:

    ```properties
    // filepath: /.env
    API_TOKEN='YOUR_TELEGRAM_BOT_API_TOKEN'
    ```

## Usage

1. Run the Telegram bot:

    ```sh
    python bot.py
    ```

2. Start a conversation with your Telegram bot and send a Medium article URL. The bot will scrape the article and send you a screenshot.

## License

This project is licensed under the MIT License.
