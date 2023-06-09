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
    
    # Start the timer
    start_time = time.time()

    try:
        # Make the API request
        response = requests.get(api_url)

        # Stop the timer and calculate the time taken
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)

        # Process the API response
        if response.status_code == 200:
            # Extract the result from the JSON response
            result = response.json().get('result', '')
            # Prepare the reply message
            reply_message = f"Status: {'❌ DEAD' if result == 'DEAD' else '✅ ALIVE'} => {card_number}"

            # Create the special button with the time taken
            keyboard = [[telegram.InlineKeyboardButton("⚙️ Time Taken", callback_data=str(time_taken))]]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)

            # Send the reply message and the button back to the user
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message, reply_markup=reply_markup)
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

# Define the function to handle the callback query for the special button
def button_callback(update, context):
    query = update.callback_query
    time_taken = query.data
    # Send the time taken as a separate message
    context.bot.send_message(chat_id=query.message.chat_id, text=f"⚙️ Time Taken: {time_taken} seconds")

# Set up the Telegram bot
bot_token = '5912062651:AAGAbfQ9OOtGM1011KWy1GUyrfPUnLaJjfQ'
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register the command and callback query handlers
check_handler = CommandHandler('check', check_command)
dispatcher.add_handler(check_handler)
dispatcher.add_handler(CallbackQueryHandler(button_callback))

# Start the bot
updater.start_polling()
