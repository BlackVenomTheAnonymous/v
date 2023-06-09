import telegram
import requests
import time
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Define the function to handle the /check command
def check_command(update, context):
    message = update.message.text
    # Extract the necessary parameters from the message
    parameters = message.split()[1].split('|')
    card_number = parameters[0]
    # Construct the API request URL
    api_url = f"https://vbvs.herokuapp.com/api?lista={card_number}"

    try:
        # Make the API request
        response = requests.get(api_url)

        # Process the API response
        if response.status_code == 200:
            # Extract the result from the JSON response
            result = response.text.strip()
            # Prepare the reply message
            reply_message = f"Status: {'❌ DEAD' if result == 'DEAD' else '✅ ALIVE'} => {card_number}"

            # Send the reply message back to the user
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
        else:
            reply_message = "An error occurred while processing the request."
            # Send the error message back to the user
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

    except requests.RequestException as e:
        # Handle request exceptions, such as network errors
        reply_message = f"An error occurred while making the API request: {str(e)}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

    except Exception as e:
        # Handle other exceptions
        reply_message = f"An error occurred: {str(e)}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

# Set up the Telegram bot
bot_token = '5912062651:AAGAbfQ9OOtGM1011KWy1GUyrfPUnLaJjfQ'
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register the command handler
check_handler = CommandHandler('check', check_command)
dispatcher.add_handler(check_handler)

# Start the bot
updater.start_polling()
