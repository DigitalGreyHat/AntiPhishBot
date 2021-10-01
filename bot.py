#default imports
import logging
import os
import signal

#Python-Telegram-Bot library
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

#Custom imports
from templates import *
from utils import *

#Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',     #take time,level,name
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#Configs
TOKEN = "YOUR_TG_BOT_TOKEN" #Get a token from the bot_father bot!
INPUT_FIELD, CHECK_URL, BULK_CHECK_URL = range(3)

def check_url(update, context):
    print(update.message.text)
    #check if url is marked as phishing
    result = check_if_red(update.message.text)
    if(result==False):
        text_msg = "*𝐒𝐈𝐍𝐆𝐋𝐄 𝐂𝐇𝐄𝐂𝐊𝐈𝐍𝐆 𝐑𝐄𝐒𝐔𝐋𝐓*\n\n*🌍 URL:* {}\n*ℹ️ Status:* *🟢 (𝙲𝙻𝙴𝙰𝙽)*".format(update.message.text)
    else:
        text_msg = "*𝐒𝐈𝐍𝐆𝐋𝐄 𝐂𝐇𝐄𝐂𝐊𝐈𝐍𝐆 𝐑𝐄𝐒𝐔𝐋𝐓*\n\n*🌍 URL:* {}\n*ℹ️ Status:* *🔴 (PHISHING)*".format(update.message.text)    
    context.bot.send_message(chat_id=update.message.chat_id, text=text_msg, parse_mode='markdown')
    templates(update, context)
    return ConversationHandler.END
def bulk_check_url(update, context):
    url_list = update.message.text
    result_template = "\n\n*🌍 URL:* {}\n*ℹ️ Status:* {}"
    final_msg = "*𝐁𝐔𝐋𝐊 𝐂𝐇𝐄𝐂𝐊𝐈𝐍𝐆 𝐑𝐄𝐒𝐔𝐋𝐓𝐒*" #Was not sure wich font you used!?
    detected_msg = "*🔴 (PHISHING)*"
    not_detected_msg = "*🟢 (𝙲𝙻𝙴𝙰𝙽)*"
    for url in url_list.split('\n'):
        result = check_if_red(url)
        if(result == False):
            final_msg += result_template.format(url, not_detected_msg)
        else:
            final_msg += result_template.format(url, detected_msg)

    context.bot.send_message(chat_id=update.message.chat_id, text=final_msg, parse_mode='markdown', disable_web_page_preview=True)
    templates(update, context)
    return ConversationHandler.END
    
#Bot Functions
#Auth Process
def login(bot, update):
    first_name  = update.message.from_user.first_name  #first name of the user messaging
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    if(user_id == YOUR_TG_ID):
        return True
    else:
        reply = '🚫You are not allowed to use this bot!!!🚫\n▪️Your Username: @{}\n▪️Your Id: {}\n\n⚠️Do not try it again or you get banned!'.format(username,user_id)
    bot.send_message(chat_id = update.message.chat_id, text = reply)      #sending an error message
    return False
    
def start(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    
    login_response = login(bot,update)
    if(login_response == True):
        first_name  = update.message.from_user.first_name
        reply = 'Hi {}, welcome to AntiPishBot.\n\nThis bot is checking url/s for phishing detection.\n\n🐍This bot is currently in beta. To use the bot please enter /dev'.format(first_name)
        bot.send_message(chat_id = update.effective_chat.id, text = reply)

def templates(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    login_response = login(bot,update)
    if(login_response == True):
        # creating list of input buttons
        keyboard = [[
            InlineKeyboardButton("Check URL", callback_data='checkURL'),
            InlineKeyboardButton("About me", callback_data='aboutMe')
        ], [InlineKeyboardButton("Developers", callback_data='devInfo')]]

        # creating a reply markup of inline keyboard options
        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending the message to the current chat id
        update.message.reply_text('What function would you like to run?', reply_markup=reply_markup)
        pass

def button(update, context):
    """
    callback method handling button press
    """
    bot: Bot = context.bot
    # getting the callback query
    query: CallbackQuery = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    
    #Get choosed button
    choosed_button = query.data
    if(choosed_button == 'checkURL'):
        keyboard = [[
        InlineKeyboardButton("Single Mode", callback_data='checkSingleURL')
    ], [InlineKeyboardButton("Bulk Mode", callback_data='checkBulkURL')]]
        
        choose_keyboard = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('Please choose a mode to check your URL/URLs!', reply_markup=choose_keyboard)
        pass
        
    elif(choosed_button == 'checkSingleURL'):
        query.edit_message_text(text='Enter URL:')
        return CHECK_URL
    elif(choosed_button == 'checkBulkURL'):
        query.edit_message_text(text='Enter your URL List (1 line = 1 URL):')
        return BULK_CHECK_URL
    elif(choosed_button == 'devInfo'):
        query.edit_message_text(text='*Developers*\nMain Dev: @BHM\n\nGo back: /dev', parse_mode='markdown')
        pass
    elif(choosed_button == 'aboutMe'):
        query.edit_message_text(text='*About Me*\nHey👋\nMy name is AntiPishBot. I was brought to alive by some developers😊\n\nCurrently I am a pretty dump bot! I can only check if an URL is red by Google Safebrowsing. Hopefully I get soon more features🙏\n\nYour AntiPishBot🤖\n\nGo back: /dev', parse_mode='markdown')
        pass
    else:
        query.edit_message_text(text='This feature is still in development! To go back please enter /dev')
    pass
    
def error(bot,update):
    logger.error("Shit!! Update {} caused error {}".format(update,update.error))
    
def stop(bot,update):
    logger.info('Stopping...')
    os.kill(os.getpid(), signal.SIGINT)

def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text='Action cancelled. Please restart the bot with /start')
    return ConversationHandler.END
    
#Main
def main():
    updater = Updater(TOKEN,use_context=True)  #take the updates
    dp = updater.dispatcher   #handle the updates
    #ConvHanlder
    conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button)],
    states={
        INPUT_FIELD: [MessageHandler(Filters.text & ~Filters.command, input_field)],
        CHECK_URL: [MessageHandler(Filters.text & ~Filters.command, check_url)],
        BULK_CHECK_URL: [MessageHandler(Filters.text & ~Filters.command, bulk_check_url)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
    dp.add_handler(conversation_handler)
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("dev", templates))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Started...")
    updater.idle()
    
if __name__=="__main__":
    main()
