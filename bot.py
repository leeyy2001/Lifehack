from dis import dis
from telegram.ext import Updater
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class VolunteerBot:
    def __init__(self, token):
        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher

        # Creating the initial commands
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('talking', self.talking))
        dispatcher.add_handler(CommandHandler('reachOut', self.reachOut))

        updater.start_polling()

    # This is the start function
    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            ''' This is the Volunteer bot. To get started finding a volunteer that suits you start /talking!\nIf you're another volunteer organization that wants to be part of the bot, /reachOut to us! ''')

    # Interactive form with the user
    def talking(self, update: Update, context: CallbackContext):
        update.message.reply_text("This functions talks to the users.")

    # For other orgs to talk to us.
    def reachOut(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "This function is for other organizations to reach out to us.")
