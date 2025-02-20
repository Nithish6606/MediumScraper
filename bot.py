import telebot
from medium_scraper import scrape_medium_article

# Initialize the Telegram bot
API_TOKEN = '5582435816:AAHsy0jonMd8IHGR4vnuVPnIpzMPhXTFEgo'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, "Welcome! Send me a Medium article URL to scrape and I'll send you a PDF.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    article_url = message.text
    pdf_path = scrape_medium_article(article_url)
    with open(pdf_path, 'rb') as pdf_file:
        bot.send_document(message.chat.id, pdf_file)


if __name__ == "__main__":
    bot.polling()
