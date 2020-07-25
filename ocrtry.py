#This is an experimental OCR bot for telegram using the python-telegram-bot Wrapper and an Open Source API for OCR found on the Internet

from telegram.ext import CommandHandler,Updater,MessageHandler,Filters
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException
from traceback import print_exc
import os
import json

CLOUDMERSIVE_API_KEY =os.environ.get("CLOUDMERSIVE_API_KEY","")


def start(update,context):
    fname = update.message.from_user.first_name
    update.message.reply_text("Hi %s, if you are stuck or don't know what to do,\nTry doing /help to look out for all available commands."%(fname))

def help(update,context):
    update.message.reply_text("Upload a photo which has clear and distinguishable english words.\nThen after confirmation of the image, OCR-chan will automatically\nsend you your text from the picture\n/start   -   Start OCR-chan!\n/help    -   Look for help!\n/userinfo    -   See your Info\n/about   -   About OCR-chan\n/chatid    -   Display the Chat ID")

def chatid(update,context):
    chatid = update.message.chat_id
    update.message.reply_text("Chat ID : "+str(chatid))

def nanikore(update,context):
    nanikore = update.message.text
    nani = "%s ??? \nNani Kore ? "%(nanikore)
    update.message.reply_text(nani)
    update.message.reply_text("😕")

def userinfo(update, context):
    fname = update.message.from_user.first_name
    lname = update.message.from_user.last_name
    uniqid = update.message.from_user.id
    usrname = update.message.from_user.username
    langcode = update.message.from_user.language_code
    dt = update.message.date
    update.message.reply_text('Unique ID : '+str(uniqid)+
                                '\nFirst Name : '+str(fname)+
                                '\nLast Name : '+str(lname)+
                                '\nUser Name : @'+str(usrname)+
                                '\nLanguage Code : '+str(langcode)+
                                '\nDate & Time : '+str(dt))

def about(update, context):
    update.message.reply_text('Creator : @iLEWDloli\n'
                               'Coded in Telegram using python-telegram-bot Wrapper\n'
                               'Hosted with ❤ in Heroku(Free account)\n'
                               'Wanna buy me a CUP of COFFEE?\nDonate Here-->https://paypal.me/adenosinetp10')


def receive(update,context):
    filename = "photo.jpg"
    fileid = update.message.photo[-1].file_id
    received = context.bot.get_file(fileid)
    received.download(filename)
    update.message.reply_text("Image received!\n🥰\n")
    api_instance =cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY
    try:
        api_response = api_instance.image_ocr_post(filename)
        sucs_percent = api_response.mean_confidence_level
        result = api_response.text_result
        update.message.reply_text("Success Percentage : "+str(sucs_percent*100)+"%\nThe text from the Image : "+str(result))
    except Exception as e:
        print_exc
        update.message.reply_text("Gomen! Error Occured.\nError Details : "+str(e))


def main():
    bot_token=os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('chatid',chatid))
    dp.add_handler(CommandHandler('userinfo',userinfo))
    dp.add_handler(CommandHandler('about',about))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, nanikore))
    dp.add_handler(MessageHandler(Filters.photo, receive))
    updater.start_polling()
    updater.idle()




if __name__ == "__main__":
    main()