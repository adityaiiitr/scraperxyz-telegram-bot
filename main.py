import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
import httpx
import threading


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
    url = f"https://www.shouttolearn.com/search?q={text}"
    
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
        check += f"{item['ids']}\n{item['title']}\n{item['link']}\n\n"
        if item['ids'] == 4:
            break

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=check.strip())

# Function to send a welcome message
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    name = user.first_name + (" " + user.last_name if user.last_name else "")
    
    welcome_text = f"Hey, *{name}*\! Welcome to ShoutToLearn Bot\!\n\nGet Help: /help"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_text, parse_mode="MarkdownV2")

# Function to send help information
def help(update: Update, context: CallbackContext):
    help_text = '''
    Help Guide For This Bot!

Bot Commands
/start - Welcome Message.
/help - This Message will get Displayed.
/contact - Contact the Admin ShoutToLearn
/isc - Class 12 related Stuff
/icse - Class 10 related Stuff
/social - Social Media Follow Links 

If You Want To Share Any Study Material, use /contact

Any Other Text Sent To This Bot Will Be Considered as a Search Query.

The Bot will Help you find if the sent text content is available on the website.

So Simple!  
    '''
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=help_text)

# Function to send contact information
def contact(update: Update, context: CallbackContext):
    contact_text = "Name: *Andhi Toofan*\nOwner, ShoutToLearn\nTelegram: @AndhiToofan\nHe is 19 years old. So, talk to him accordingly!"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=contact_text, parse_mode="MarkdownV2")

# Function to send ISC-related information
def isc(update: Update, context: CallbackContext):
    inter_text = '''
*List Of ISC Content:*

[Echoes](https://bot.shouttolearn.com/echoes)   [Reverie](https://bot.shouttolearn.com/reverie)   [Tempest](https://bot.shouttolearn.com/tempest)
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=inter_text,
                             parse_mode="MarkdownV2")

# Function to send ICSE-related information
def icse(update: Update, context: CallbackContext):
    high_text = '''
*List Of ICSE Content:*

[Treasure Trove Workbook Stories](https://bot.shouttolearn.com/stories)   
[Treasure Trove Workbook Poems](https://bot.shouttolearn.com/poems)
[Merchant Of Venice](https://bot.shouttolearn.com/mov)
[Ekanki Sanchay](https://bot.shouttolearn.com/ekanki)   [Sahitya Sagar](https://bot.shouttolearn.com/sahitya)
[Geography](https://bot.shouttolearn.com/geo)    [History](https://bot.shouttolearn.com/history)
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=high_text,
                             parse_mode="MarkdownV2")

# Function to send social media links
def social(update: Update, context: CallbackContext):
    social_text = '''
    Follow Official Social Media Handles Only!
    
[Facebook](https://bot.shouttolearn.com/fb)   [Instagram](https://bot.shouttolearn.com/ig)   [Twitter](https://bot.shouttolearn.com/tw)
*Telegram:* @ShoutToLearn
    '''
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=social_text, parse_mode="MarkdownV2")

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
    # st.text("Bot is running...")

    updater.idle()

if __name__ == "__main__":
    TOKEN = os.getenv('BOT_TOKEN')
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=main)
    bot_thread.start()
    # main()
