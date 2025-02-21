import telebot
import logging
import os
import asyncio
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
    user_name = message.chat.first_name or "User"  # Fallback if no first name
    greeting_text = f"Hello, {user_name}! 👋\nSend me a Medium article URL, and I'll send Screenshot."

    bot.reply_to(message, greeting_text)
    logging.info(
        f"Sent welcome message to {user_name} (User ID: {message.chat.id})")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_name = message.chat.first_name or "User"
    article_url = message.text
    logging.info(
        f"Received URL: {article_url} from {user_name} (User ID: {message.chat.id})")

    try:
        screenshot_path = asyncio.run(
            scrape_medium_article(article_url))  # ✅ Use asyncio.run()

        if screenshot_path:
            with open(screenshot_path, 'rb') as screenshot_file:
                bot.send_document(message.chat.id, screenshot_file)
                logging.info(
                    f"Sent screenshot {screenshot_path} to {user_name} (User ID: {message.chat.id})")

            os.remove(screenshot_path)  # Delete screenshot after sending
            logging.info(f"Deleted screenshot {screenshot_path}")
        else:
            bot.reply_to(
                message, f"Sorry {user_name}, I couldn't process the article. Please try again.")
            logging.error(
                f"Failed to process the article for URL: {article_url}")

    except Exception as e:
        logging.error(f"Error processing article: {e}")
        bot.reply_to(
            message, f"Oops {user_name}, something went wrong. Please try again later.")


if __name__ == "__main__":
    logging.info("Starting bot")
    bot.polling(none_stop=True)
