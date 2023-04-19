from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

CHOOSING, TYPING_REPLY, TYPING_CHOICE,  TIMER = range(4)



class ConversationHandlerFactory():
    def __init__(self, entrypoint, choosing, typing_choice, typing_reply, timer, fallback) -> None:
        self.entrypoint = entrypoint
        self.choosing = choosing
        self.typing_choice = typing_choice
        self.typing_reply = typing_reply
        self.timer = timer
        self.fallback = fallback
        
    def get(self):
        return ConversationHandler(
        entry_points=[CommandHandler("start", self.entrypoint)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Modelo|Direção|Quilometragem|Tipo de Câmbio|Tipo de Combustível|Ano)$"), self.choosing,
                ),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")), self.typing_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")),
                    self.typing_reply,
                )
            ],
            TIMER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.timer)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Pronto$"), self.fallback)],
    )