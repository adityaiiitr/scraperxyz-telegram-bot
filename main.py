import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
import httpx


# Load environment variables
load_dotenv()

# Initialize the logging module
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a dataclass for search results
@dataclass
class SearchResults:
    ids: int
    title: str
    link: str

# Function to get HTML content from a website
def get_html(text: str):
    logger.info(f"Searched Text: {text}")
    url = f"https://www.scraperxyz.com/search?q={text}"
    
    with httpx.Client() as client:
        resp = client.get(url)

    html = HTMLParser(resp.text)
    return html

# Function to parse search results from HTML
def parse_results(html):
    title_list = html.css("h2.pTtl.aTtl.sml")
    results = []
    
    for i, item in enumerate(title_list, start=1):
        new_item = SearchResults(
            ids=i,
            title=item.css_first("a").text().strip(),
            link=item.css_first("a").attributes.get('href')
        )
        results.append(asdict(new_item))
        if i == 4:
            break
    
    return results

# Function to handle text messages
def echo(update: Update, context: CallbackContext):
    string = update.message.text.strip()

    html = get_html(string)
    result = parse_results(html)
    
    check = "Search Results:\n"
    for item in result:
        check += f"🔗 [{item['title']}]({item['link']})\n"
        if item['ids'] == 4:
            break

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=check.strip(),disable_web_page_preview=True, parse_mode="MarkdownV2")

# Function to send a welcome message
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    user_id = user.id
    chat_id = chat.id
    username = user.username if user.username else "N/A"

    logger.info(f"User started a conversation - User ID: {user_id}, Chat ID: {chat_id}, Username: {username}")

    user = update.effective_user
    name = user.first_name + (" " + user.last_name if user.last_name else "")

    
    welcome_text = f'''
👋 **Welcome to scraperxyz Bot, {name}\!**

I\'m your friendly study companion, here to make learning a breeze\. 📚✨

Need assistance? Just say the word:

🚀 Type `/help` to unlock a treasure trove of bot features\.

Let's embark on this learning journey together\! Feel free to ask questions or explore the commands\. 🤖💬

Happy learning, {name}\! 📖🌟

'''
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_text, parse_mode="MarkdownV2")

# Function to send help information
def help(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    user_id = user.id
    chat_id = chat.id
    username = user.username if user.username else "N/A"

    logger.info(f"User requested help - User ID: {user_id}, Chat ID: {chat_id}, Username: {username}")

    help_text = '''
🤖 **Bot Help Guide**

Welcome to the scraperxyz Bot\! Here are some commands to supercharge your learning experience:

🚀 `/start` \- Get a warm welcome message\.

ℹ️ `/help` \- Access this informative guide anytime\.

📞 `/contact` \- Connect with Admin scraperxyz\.

📚 `/isc` \- Dive into Class 12\-related resources\.

📘 `/icse` \- Explore Class 10\-related materials\.

🌐 `/social` \- Follow us on social media\.

If you\'re eager to share study materials, simply use `/contact`\. We\'d love to hear from you\!

Don\'t worry about complicated instructions\. Just send any text, and our bot will magically find related content on our website\. It\'s that simple and tech\-savvy\!

Happy learning\! 📖✨
'''
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=help_text, parse_mode="MarkdownV2", disable_web_page_preview=True)

# Function to send contact information
def contact(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    user_id = user.id
    chat_id = chat.id
    username = user.username if user.username else "N/A"

    logger.info(f"User requested contact information - User ID: {user_id}, Chat ID: {chat_id}, Username: {username}")

    contact_text = '''
🚀 **Meet the Mastermind Behind scraperxyz**

Name: *Andhi Toofan* 💥
Role: Founder and Captain of scraperxyz 🚀
Telegram: [@AndhiToofan](https://telegram.me/AndhiToofan)

Age is just a number\, and for Andhi Toofan\, it\'s 19\! 🎉 Feel free to connect\, chat\, and share your thoughts\. He\'s got the energy and enthusiasm to make your learning experience out of this world\! 🌟💬

Ready to join the adventure? Reach out and let\'s explore the world of knowledge together\! 📚🌏
'''
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=contact_text, parse_mode="MarkdownV2", disable_web_page_preview=True)

# Function to send ISC-related information
def isc(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    user_id = user.id
    chat_id = chat.id
    username = user.username if user.username else "N/A"

    logger.info(f"User requested ISC-related information - User ID: {user_id}, Chat ID: {chat_id}, Username: {username}")

    inter_text = '''
📚 *List Of ISC Content:*

🔗 [Echoes](https://bot.scraperxyz.com/echoes)
🔗 [Reverie](https://bot.scraperxyz.com/reverie)
🔗 [Tempest](https://bot.scraperxyz.com/tempest)
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=inter_text,
                             parse_mode="MarkdownV2", disable_web_page_preview=True)

# Function to send ICSE-related information
def icse(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    user_id = user.id
    chat_id = chat.id
    username = user.username if user.username else "N/A"

    logger.info(f"User requested ICSE-related information - User ID: {user_id}, Chat ID: {chat_id}, Username: {username}")

    high_text = '''
📚 *List Of ICSE Content:*

🔗 [Treasure Chest Poems](https://www.scraperxyz.com/p/workbook-answers-of-treasure-chest-poems.html)
🔗 [Treasure Chest Stories](https://www.scraperxyz.com/p/workbook-answers-of-treasure-chest.html)
🔗 [Treasure Trove Workbook Stories](https://bot.scraperxyz.com/stories)
🔗 [Treasure Trove Workbook Stories](https://bot.scraperxyz.com/stories)
🔗 [Treasure Trove Workbook Poems](https://bot.scraperxyz.com/poems)
🔗 [Merchant Of Venice](https://bot.scraperxyz.com/mov)
🔗 [Ekanki Sanchay](https://bot.scraperxyz.com/ekanki)
🔗 [Sahitya Sagar](https://bot.scraperxyz.com/sahitya)
🔗 [Geography](https://bot.scraperxyz.com/geo)
🔗 [History](https://bot.scraperxyz.com/history)
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=high_text,
                             parse_mode="MarkdownV2", disable_web_page_preview=True)

# Function to send social media links
def social(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    user_id = user.id
    chat_id = chat.id
    username = user.username if user.username else "N/A"

    logger.info(f"User requested Social Media Handles - User ID: {user_id}, Chat ID: {chat_id}, Username: {username}")

    social_text = '''
📱 Follow Official Social Media Handles Only\!

📘 [Facebook](https://bot.scraperxyz.com/fb)
📷 [Instagram](https://bot.scraperxyz.com/ig)
🐦 [Twitter](https://bot.scraperxyz.com/tw)
📢 *Telegram:* @scraperxyz
    '''
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=social_text, parse_mode="MarkdownV2", disable_web_page_preview=True)

# Function to handle unknown commands
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

# Main function to start the bot
def main():
    TOKEN = os.getenv('BOT_TOKEN')
    updater = Updater(
        token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('contact', contact))
    dispatcher.add_handler(CommandHandler('isc', isc))
    dispatcher.add_handler(CommandHandler('icse', icse))
    dispatcher.add_handler(CommandHandler('social', social))

    # Message Handler
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # Unknown Commands Handler
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # Start the bot
    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    # TOKEN = os.getenv('BOT_TOKEN')
    main()
