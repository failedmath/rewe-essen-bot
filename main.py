import logging
import os

import requests
import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger('bot')

# The sensitive data is written in the .env file, in the format KEY='KEY'
# Dotenv helps to get the data from the local folder, otherwise the computer will get some other .env
env_path = os.path.join(os.path.dirname(__file__), ".env")  # get the .env file from your folder
load_dotenv(dotenv_path=env_path)

# Authorisation in twitter
TOKEN = os.getenv("ACCESS_TOKEN")
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")


class ShoppingCart:
    def __init__(self):
        self.shopping_list = []
        self.ingredients = []
        self.attendees = 2
        self.allergies = None
        self.address = None
        self.logs = []


ShoppingCart = ShoppingCart()


# Functions
def start(update, context):
    ShoppingCart.shopping_list = []
    ShoppingCart.ingredients = []
    ShoppingCart.attendees = 2
    ShoppingCart.logs = []
    reply_markup = telegram.ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi, what do you want to cook today?")
    context.bot.send_message(chat_id=update.message.chat_id, text="Just type /recipe and the dish name. "
                                                                  "If you want to update number of attendees, type /attendees and number of people"
                                                                  "You can check your shopping cart with /shoppinglist ."
                                                                  "To finish, type /readytoorder",
                             reply_markup=reply_markup)
    context.bot.send_document(chat_id=update.message.chat_id, document="https://media.giphy.com/media/eSQKNSmg07dHq/giphy.gif")

def set_attendee_number(update, context):
    attendees = " ".join(context.args)
    try:
        attendees = int(attendees)
        context.bot.send_message(chat_id=update.message.chat_id, text=f"You will be {attendees} people, great! ")
    except:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Please type /attendees and the number of people ")


def echo(update, context):

    ShoppingCart.logs.append(update.message.text)
    if update.message.text in ShoppingCart.ingredients:
        ShoppingCart.shopping_list.append(update.message.text)
        context.bot.send_message(chat_id=update.message.chat_id, text=f'You added {update.message.text} to the shopping list')
    else:
        pass
        # context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def getrecipe(update, context):
    food = " ".join(context.args)
    if food == "":
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"You didn't mention what you want, let's get something random")
        food = "chicken"
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'You wish to cook {food}')

    headers = {'X-API-TOKEN': APP_KEY}
    post_string = "https://api.edamam.com/search?q=" + food + "&app_id=" + APP_ID + "&app_key=" + APP_KEY
    r = requests.post(post_string, headers=headers)
    logger.info(r.json())
    try:
        full_recipe = r.json()['hits'][0]['recipe']
        ingredients = full_recipe['ingredientLines']
        name = full_recipe['label']
        context.bot.send_message(chat_id=update.message.chat_id, text=f'We found for you recipe of {name}')
        context.bot.send_message(chat_id=update.message.chat_id, text=f'For this you need {", ".join(ingredients)}')
        keyboard_list = [[i] for i in ingredients]
        keyboard_list.append(['/recipe'])
        keyboard_list.append(['/shoppinglist'])
        keyboard_list.append(['/readytoorder'])
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard_list)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Do you have all ingredients at home? Pick the ones that are missing",
                                 reply_markup=reply_markup)
        ShoppingCart.ingredients.extend(ingredients)
    except:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Unfortunately, we cannot get this one. Please, try again.')


def get_shopping_list(update, context):
    shopping_list = list(set(ShoppingCart.shopping_list))
    if len(shopping_list) == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Your shopping list is empty')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'You have in your shopping cart: {", ".join(shopping_list)}')


def ready_to_order(update, context):
    reply_markup = telegram.ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, text=f'Ready to deliver to your address!', reply_markup=reply_markup)
    context.bot.send_document(chat_id=update.message.chat_id, document="https://media.giphy.com/media/3nbxypT20Ulmo/giphy.gif")


def test(update, context):
    pass

# create updater and dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# stack functions together
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

attendee_handler = CommandHandler('attendees', set_attendee_number)
dispatcher.add_handler(attendee_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

recipe_handler = CommandHandler('recipe', getrecipe)
dispatcher.add_handler(recipe_handler)

shopping_list_handler = CommandHandler('shoppinglist', get_shopping_list)
dispatcher.add_handler(shopping_list_handler)

order_handler = CommandHandler('readytoorder', ready_to_order)
dispatcher.add_handler(order_handler)

# test_handler = CommandHandler('test', test, pass_args=True)
# dispatcher.add_handler(test_handler)

updater.start_polling()
