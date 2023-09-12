import logging
from posixpath import split
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import telegram


# Web Scrapping using HTTPX and Selectolax
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict

from dotenv import load_dotenv
load_dotenv() 


# Code For Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------WEB SCRAPING BEGINS---------------------
#  For any Random Search Result


@dataclass
class searchResults:
    ids: int
    title: str
    link: str


def get_html(text):
    print(f"Searched Text: {text}")
    url = f"https://www.shouttolearn.com/search?q={text}"
    resp = httpx.get(url)
    html = HTMLParser(resp.text)
    # print("Fetched HTML")
    return html


def parseResults(html):
    # print(html)
    title_list = html.css("h2.pTtl.aTtl.sml")
    # print("Fetched Required TAgs")
    print(title_list)
    results = []
    i = 1
    for item in title_list:
        new_item = searchResults(
            ids=i,
            title=item.css_first("a").text().strip(),
            link=item.css_first("a").attributes.get('href')
        )
        i = i+1
        results.append(asdict(new_item))
    # print("Required Data Extracted")
    return results

# -------------WEB SCRAPING ENDS-------------


def echo(update: Update, context: CallbackContext):
    string = update.message.text.strip()

    html = get_html(string)
    # print("get html completed")
    result = parseResults(html)
    # print("useful extracted data arrived")
    # print(result)
    check = "Search Results: "
    for item in result:
        check = check + str(item['ids'])+"\n" + \
            item['title']+'\n'+item['link']+"\n\n"
        if(item['ids'] == 4):
            break
    print(check)

    # search_text = "Open this link: https://www.shouttolearn.com/search?q="
    # for i in string:
    #     search_text = search_text+i+"+"
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text=search_text[0:len(search_text)-1])
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=check[0:len(check)-1])

# https://www.shouttolearn.com/search?q=Sahitya+Sagar


def start(update: Update, context: CallbackContext):
    name = ""
    try:
        name = update.effective_chat.first_name + " " + update.effective_chat.last_name
        print(f"Name: {name}")
    except TypeError:
        name = update.effective_chat.first_name
        print(f"Name: {name}")
    
    welcome_text = "Hey, *{}* Welcome to ShoutToLearn Bot\! \n\nGet Help\: /help".format(
        name)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_text, parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2)


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

If You Want To Share Any Study Material /contact

Any Other Text Sent To This Bot Will Be Considered as Search Query.

Bot will Help you find the sent text content is available on website.

So Simple!  

'''
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=help_text)


def contact(update: Update, context: CallbackContext):
    contact_text = "Name: *Andhi Toofan*\nOwner\, ShoutToLearn\nTelegram: \@AndhiToofan\nHe is 19 years old\. So\, Talk to him accordingly\!"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=contact_text, parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2)


def isc(update: Update, context: CallbackContext):
    inter_text = '''
*List Of ISC Content \:\-*

[*Echoes*](https://bot.shouttolearn.com/echoes)   [*Reverie*](https://bot.shouttolearn.com/reverie)   [*Tempest*](https://bot.shouttolearn.com/tempest)
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=inter_text,
                             parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2)


def icse(update: Update, context: CallbackContext):
    high_text = '''
*List Of ICSE Content \:\-*

[*Treasure Trove Workbook Stories*](https://bot.shouttolearn.com/stories)   

[*Treasure Trove Workbook Poems*](https://bot.shouttolearn.com/poems)

[*Merchant Of Venice*](https://bot.shouttolearn.com/mov)

[*Ekanki Sanchay*](https://bot.shouttolearn.com/ekanki)   [*Sahitya Sagar*](https://bot.shouttolearn.com/sahitya)

[*Geography*](https://bot.shouttolearn.com/geo)    [*History*](https://bot.shouttolearn.com/history)  


    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=high_text,
                             parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2)


def social(update: Update, context: CallbackContext):
    social_text = '''
    Follow Oficial Social Media Handles Only\!
    
[*Facebook*](https://bot.shouttolearn.com/fb)   [*Instagram*](https://bot.shouttolearn.com/ig)   [*Twitter*](https://bot.shouttolearn.com/tw)
*Telegram:* \@ShoutToLearn
    '''
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=social_text, parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2)


# def caps(update: Update, context: CallbackContext):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


# def error(bot, update):
#     logger.error("Update '%s' caused error '%s' ", update, update.error)

import os
def main():
    updater = Updater(
        token=os.getenv('BOT_TOKEN'), use_context=True)

    dispatcher = updater.dispatcher
    # Command Handler

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('contact', contact))
    dispatcher.add_handler(CommandHandler('isc', isc))
    dispatcher.add_handler(CommandHandler('icse', icse))
    dispatcher.add_handler(CommandHandler('social', social))

    # Message Handler
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    # # CAPS HAndler
    # caps_handler = CommandHandler('caps', caps)
    # dispatcher.add_handler(caps_handler)
    # Unknown Commands Handler
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
