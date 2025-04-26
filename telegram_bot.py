from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import manager
import motor_traffic
import motor_details
import ktmb
import telegram_extract
import os
import get_weather_forecast_information  # Import the get_weather_forecast module
from dotenv import load_dotenv
import os
load_dotenv()

# Define the command handler for running manager.py
async def run_manager(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
    await message.reply_text('Running manager.py...', parse_mode=None)
    try:
        await manager.run_scripts()
        await message.reply_text('manager.py completed successfully.', parse_mode=None)

        # Send the merged_data.csv file
        dir_path = r'combined_data'
        file_path = os.path.join(dir_path, 'merged_data.csv')
        if os.path.exists(file_path):
            await message.reply_document(document=open(file_path, 'rb'))
        else:
            await message.reply_text('Merged Data not found.', parse_mode=None)

    except Exception as e:
        await message.reply_text('Error running manager.py:', parse_mode=None)
        await message.reply_text(str(e), parse_mode=None)

# Define the command handler for running motor_traffic.py
async def run_motor_traffic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
    await message.reply_text('Running motor_traffic.py...', parse_mode=None)
    try:
        await motor_traffic.main()
        await message.reply_text('motor_traffic.py completed successfully.', parse_mode=None)

        # Send images from the specified directory
        image_dir = r'motor_traffic_data'
        for filename in os.listdir(image_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(image_dir, filename)
                with open(image_path, 'rb') as image_file:
                    await message.reply_photo(photo=image_file)

    except Exception as e:
        await message.reply_text('Error running motor_traffic.py:', parse_mode=None)
        await message.reply_text(str(e), parse_mode=None)

async def get_ktmb_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
    await message.reply_text('Getting KTMB updates...', parse_mode=None)
    try:
        await ktmb.main()
        await message.reply_text('KTMB updates collected successfully.', parse_mode=None)

        # Send the ktmb_data.csv file
        dir_path = r'combined_data'
        file_path = os.path.join(dir_path, 'train_data.csv')
        if os.path.exists(file_path):
            await message.reply_document(document=open(file_path, 'rb'))
        else:
            await message.reply_text('KTMB Data not found.', parse_mode=None)

    except Exception as e:
        await message.reply_text('Error getting KTMB updates:', parse_mode=None)
        await message.reply_text(str(e), parse_mode=None)

async def get_telegram_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
    await message.reply_text('Getting Telegram updates...', parse_mode=None)
    try:
        await telegram_extract.main()
        await message.reply_text('Telegram updates collected successfully.', parse_mode=None)

        # Send the telegram_messages.csv file
        dir_path = r'combined_data'
        file_path = os.path.join(dir_path, 'telegram_messages.csv')
        if os.path.exists(file_path):
            await message.reply_document(document=open(file_path, 'rb'))
        else:
            await message.reply_text('Telegram Data not found.', parse_mode=None)

    except Exception as e:
        await message.reply_text('Error getting Telegram updates:', parse_mode=None)
        await message.reply_text(str(e), parse_mode=None)

async def get_motor_traffic_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
    await message.reply_text("Getting motor traffic data...", parse_mode=None)
    try:
        await motor_details.main()
        await message.reply_text('Motor traffic data collected successfully.', parse_mode=None)

        # Send the motor_traffic_data.csv file
        dir_path = r'combined_data'
        file_path = os.path.join(dir_path, 'motor_traffic_data.csv')
        if os.path.exists(file_path):
            await message.reply_document(document=open(file_path, 'rb'))
        else:
            await message.reply_text('Traffic Data not found.', parse_mode=None)

    except Exception as e:
        await message.reply_text('Error getting motor traffic data:', parse_mode=None)
        await message.reply_text(str(e), parse_mode=None)

# Define the command handler for getting weather forecast
async def get_weather_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    message = update.message or update.callback_query.message
    await message.reply_text("Getting weather forecast...", parse_mode=None)
    try:
        forecast = await get_weather_forecast_information.main()
        await message.reply_text('Weather forecast collected successfully.', parse_mode=None)
        await message.reply_text("There will be " +forecast + " at Woodlands", parse_mode=None)

    
    except Exception as e:
        await message.reply_text('Error getting weather forecast:', parse_mode=None)
        await message.reply_text(str(e), parse_mode=None)
    
# Start command with menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ['Run Manager - Manage and merge data'],
        ['Motor Traffic - Get traffic images'],
        ['Motor Traffic Details - Traffic CSV'],
        ['KTMB Updates - Train data updates'],
        ['Telegram Updates - Group messages'],
        ['Weather Forecast - Get weather forecast'],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text(
        "Please choose an option:\n"
        "- Run Manager: Collect and merge data.\n"
        "- Motor Traffic: Retrieve traffic images.\n"
        "- Motor Traffic Details: Generate traffic CSV data.\n"
        "- KTMB Updates: Get train data updates.\n"
        "- Telegram Updates: Extract group messages.\n"
        "- Weather Forecast: Get weather forecast.",
        reply_markup=reply_markup,
        parse_mode=None
    )

# Handle text-based menu options
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text.startswith('Run Manager'):
        await run_manager(update, context)
    elif text.startswith('Motor Traffic - Get traffic images'):
        await run_motor_traffic(update, context)
    elif text.startswith('Motor Traffic Details'):
        await get_motor_traffic_details(update, context)
    elif text.startswith('KTMB Updates'):
        await get_ktmb_updates(update, context)
    elif text.startswith('Telegram Updates'):
        await get_telegram_updates(update, context)
    elif text.startswith('Weather Forecast'):
        await get_weather_forecast(update, context)
    else:
        await update.message.reply_text("Sorry, I didn't understand that command.", parse_mode=None)

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_ID_TOKEN")#update your telegram bot token id
    application = Application.builder().token(token).build()

    # Command handler for /start
    application.add_handler(CommandHandler('start', start))
    # Command handler for /menu
    application.add_handler(CommandHandler('menu', start))
    # Command handler for /run_manager
    application.add_handler(CommandHandler('run_manager', run_manager))
    # Command handler for /run_motor_traffic
    application.add_handler(CommandHandler('run_motor_traffic', run_motor_traffic))
    # Command handler for /get_motor_traffic_details
    application.add_handler(CommandHandler('get_motor_traffic_details', get_motor_traffic_details))
    # Command handler for /get_ktmb_updates
    application.add_handler(CommandHandler('get_ktmb_updates', get_ktmb_updates))
    # Command handler for /get_telegram_updates
    application.add_handler(CommandHandler('get_telegram_updates', get_telegram_updates))
    # Command handler for /get_weather_forecast
    application.add_handler(CommandHandler('get_weather_forecast', get_weather_forecast_information))
    # Text handler for menu options
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == '__main__':
    main()