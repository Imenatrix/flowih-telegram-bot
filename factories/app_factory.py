from dotenv import dotenv_values
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
)
from factories.conversation_handler_factory import ConversationHandlerFactory
from factories.chat_factory import ChatFactory
from utils.timer_util import set_timer


config = dict(dotenv_values(".env"))

class AppFactory():
    async def _show_help(self,update: Update) -> None:
        await update.effective_message.reply_text(
            "Comandos aceitos:\n"+
            "- /start: Começa o fluxo\n" +
            "- /help: Mostra comandos\n"
        )
    def _get_conv_handler(self,chat):
        return ConversationHandlerFactory(           
            entrypoint=chat.start, 
            choosing=chat.regular_choice, 
            typing_choice=chat.regular_choice, 
            typing_reply=chat.received_information, 
            timer=set_timer, 
            fallback=chat.done).get()

    def run(self, handlers=[], chat=ChatFactory())->None:
            app = Application.builder().token(config['TOKEN']).build()
            
            app.add_handler(CommandHandler("help", self._show_help))
            app.add_handler(self._get_conv_handler(chat))
            
            if len(handlers) > 0:
                for i in handlers:
                    app.add_handler(i)

            # Run the bot until the user presses Ctrl-C
            app.run_polling()