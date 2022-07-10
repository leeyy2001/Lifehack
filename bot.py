from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import animalData
import socialData
import environmentData

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class VolunteerBot:
    def __init__(self, token):
        # Storing the data for easy access
        self.data = {
            "animals": animalData.animal_organisations,
            "social": socialData.social_organisations,
            "environment": environmentData.environmental_organisations,
        }

        # Object to store data
        self.userData = {
            "volType": None,
            "location": None,
        }

        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher

        self.LOCATION, self.VOLTYPE = range(2)

        # Creating the conversation handler that asks the user for a location.
        conversationVol = ConversationHandler(
            entry_points=[CommandHandler(
                'talking', self.startConvo)],
            states={
                self.VOLTYPE: [MessageHandler(
                    Filters.text & (~Filters.command), self.volType)],
                self.LOCATION: [MessageHandler(
                    Filters.text & (~Filters.command), self.location)],
            },
            fallbacks=[CommandHandler(
                'start', self.start)]
        )

        # Creating the initial commands
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(conversationVol)
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

        update.message.bot.send_photo(update.message.chat_id, open(r"C:\Users\yylee\Downloads\lifehack image.webp", 'rb')) and update.message.reply_text(
            "Where would you like to volunteer at?\nType:\n'n' for North\n'ne' for Northeast\n'c' for Central\n'e' for East\n'w' for West.")

        return self.LOCATION

    # Asking the users for their preferred location and returning data fitting the location and volunteer type.
    def location(self, update: Update, context: CallbackContext):
        self.userData['location'] = update.message.text.lower()

        # Error handling in the event that the data is wrong
        try:
            data = self.data[self.userData['volType']
                             ][self.userData['location']]
            update.message.reply_text(
                "Thanks for using the application here are your results!") and update.message.reply_text(f"{data}") and update.message.reply_text("Find more opportunities by /talking to me!")
        except KeyError:
            update.message.reply_text(
                "The location or volunteer type you entered was wrong. Try /talking to me again!")

            return ConversationHandler.END
        except:
            update.message.reply_text(
                "An error has occurred :(. Try /talking to me again!")

            return ConversationHandler.END

        return ConversationHandler.END

    # For other orgs to talk to us.
    def reachOut(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Contact us at yylee.work@gmail.com, YZ's and Solaiy's email.")
