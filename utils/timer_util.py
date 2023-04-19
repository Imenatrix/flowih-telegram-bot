import time
from telegram import  Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,

)

async def set_timer(update=Update) -> None:
    """
        Cria uma job na fila
    """
    interval = convert_to_seconds()
        
    try:
        if interval < 0:
            await update.effective_message.reply_text("Intervalo inválido!")
            while True:
                alarm(interval, update)
                time.sleep(interval)
    except Exception:
        await update.effective_message.reply_text("Ops! houve um erro, tente novamente!")
        return ConversationHandler.END

        

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """ 
        Manda a notificação.
    """
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")
    
    
def convert_to_seconds(update: Update,interval:int=60,) -> int:
    if "hora" in update.message.text:
        return  float(str(update.message.text).split(" ")[0]) * 60 * 60
    if "minuto" in update.message.text:
        return float(str(update.message.text).split(" ")[0]) * 60
