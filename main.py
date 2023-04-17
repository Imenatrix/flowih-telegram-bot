from telegram.ext import *
from dotenv import dotenv_values
    
print('Starting a bot....')
     
async def start_commmand(update, context):
    await update.message.reply_text('Hello World!')

if __name__ == '__main__':
    config = dict(dotenv_values(".env"))
    application = Application.builder().token(config['TOKEN']).build()

    # Commands
    application.add_handler(CommandHandler('start', start_commmand))

    # Run bot
    application.run_polling(1.0)