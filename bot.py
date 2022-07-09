from ast import Call
from re import L
from telegram.ext import Updater
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class VolunteerBot:
    def __init__(self, token):
        # Object to store data
        self.userData = {
            "volType": None,
            "location": None,
        }

        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher

        self.LOCATION, self.VOLTYPE, self.DATA = range(3)

        conversationVol = ConversationHandler(
            entry_points=[CommandHandler('talking', self.startConvo)],
            states={
                self.VOLTYPE: [MessageHandler(
                    Filters.text & (~Filters.command), self.volType)],
                self.LOCATION: [MessageHandler(
                    Filters.text & (~Filters.command), self.location)],
                self.DATA: [MessageHandler(
                    Filters.text & (~Filters.command), self.data)]
            },
            fallbacks=[CommandHandler('start', self.start)]
        )

        # Creating the initial commands
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(conversationVol)
        # dispatcher.add_handler(CommandHandler('talking', self.talking))
        dispatcher.add_handler(CommandHandler('reachOut', self.reachOut))

        updater.start_polling()

    # This is the start function
    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            ''' This bot serves to recommend various community service projects, based on the user's preferred location and interests.\n For prospective volunteers, type /talking to find an organisation that suits you.\n If you're a volunteer organization that wants to be part of the bot, type /reachOut for more information!''')

    # Interactive form with the user
    def startConvo(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Let us know what type of volunteer work you enjoy!\nType either 'Environment', 'Social' or 'Animals'.")

        return self.VOLTYPE

    def volType(self, update: Update, context: CallbackContext):
        self.userData["volType"] = update.message.text.lower()

        update.message.reply_text(
            "Where would you like to volunteer at?\nType:\n'n' for North\n'c' for Central\n'e' for East\n'w' for West.")

        return self.LOCATION

    def location(self, update: Update, context: CallbackContext):
        self.userData['location'] = update.message.text.lower()

        update.message.reply_text(
            "Thanks for using the application here are your results!")

        print(self.userData)
        return self.DATA

    def data(self, update: Update, context: CallbackContext):
        update.message.reply_text("Here is the data")

        return ConversationHandler.END

    # For other orgs to talk to us.
    def reachOut(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "This function is for other organizations to reach out to us.")
