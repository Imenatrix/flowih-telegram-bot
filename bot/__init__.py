from bot.utils import show_help, unset_client_interval, unset_process
from settings import (
    config,
    CHOOSING,
    TYPING_CHOICE,
    TYPING_REPLY,
    TIMER
)
from bot.states import (
    entrypoint,
    choosing_state,
    timer_state,
    typing_choice_state,
    typing_reply_state,
    fallback_state
)
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
)


def init():
    app = Application.builder().token(config['TOKEN']).build()

    app.add_handler(CommandHandler("help", show_help))
    app.add_handler(CommandHandler("r", unset_process))
    app.add_handler(CommandHandler("unset", unset_client_interval))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", entrypoint)],
        states={
            CHOOSING: choosing_state(),
            TYPING_CHOICE: typing_choice_state(),
            TYPING_REPLY: typing_reply_state(),
            TIMER: timer_state()
        },
        fallbacks=fallback_state(),
    ))
    # Roda o bot até alguém interromper o script com Ctrt + C
    app.run_polling()
