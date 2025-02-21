import telebot
import logging
import os
from dotenv import load_dotenv
from medium_scraper import scrape_medium_article

# Load environment variables from .env file
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

# Initialize the Telegram bot
bot = telebot.TeleBot(API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, "Welcome! Send me a Medium article URL to scrape and I'll send you a screenshot.")
    logging.info(f"Sent welcome message to user {message.chat.id}")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    article_url = message.text
    logging.info(f"Received URL: {article_url} from user {message.chat.id}")
    screenshot_path = scrape_medium_article(article_url)
    if screenshot_path:
        with open(screenshot_path, 'rb') as screenshot_file:
            bot.send_document(message.chat.id, screenshot_file)
            logging.info(
                f"Sent screenshot {screenshot_path} to user {message.chat.id}")
        # Delete the screenshot after sending
        os.remove(screenshot_path)
        logging.info(f"Deleted screenshot {screenshot_path}")
    else:
        bot.reply_to(
            message, "Failed to scrape the article. Please try again.")
        logging.error(f"Failed to scrape the article for URL: {article_url}")


if __name__ == "__main__":
    logging.info("Starting bot")
    bot.polling()
