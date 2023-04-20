

import logging
import time
from typing import Dict
import threading
from telegram import ReplyKeyboardRemove, Update
from conf import (
    TYPING_REPLY,
    CHOOSING,
    TIMER,
    REPLY_DEFAULT,
    url_filters,
    markup,
    interval_markup,
    strwheel_markup,
    gear_markup,
    gas_markup
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
        Pede o input do usuario sobre o topico escolhido
    """
    logging.info("regular choice")

    try:
        text = update.message.text
        context.user_data["choice"] = text
        reply = REPLY_DEFAULT + f" para {text.lower()}: "
        await validate_choices(reply, text, update, context)
    except Exception as e:
        show_error(update, context)
        return ConversationHandler.END
    return TYPING_REPLY


async def regular_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
        Guarda a info e pergunta a proxima
    """
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Filtros escolhidos:"
        f"{_facts_to_str(user_data)}",
        reply_markup=markup,
    )

    return CHOOSING


def _facts_to_str(user_data: Dict[str, str]) -> str:
    """
        Formata as escolhas em formato de lista.
    """
    url_filters = {key.lower().replace(" ", "_"): value for key,
                   value in user_data.items()}
    print(url_filters)
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def done_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
        Mostra os filtros escolhidos.
    """
    logging.info("done_fallback")

    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"Esses foram seus filtros: {_facts_to_str(user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.message.reply_text(
        "Agora, escolha o intervalo para ser notificado:",
        reply_markup=interval_markup,
    )
    return TIMER


async def show_help(self, update: Update) -> None:
    await update.effective_message.reply_text(
        "Comandos aceitos:\n" +
        "- /start: Começa o fluxo\n" +
        "- /help: Mostra comandos\n" +
        "- /unset: Remove intervalo configurado\n"
    )


async def alarm(interval, update: Update) -> None:
    """ 
        Manda a notificação.
    """
    logging.info("NO ALARM")
    await update.effective_message.reply_text(f"{interval} segundos passaram! Aeee!")


def _convert_to_seconds(update: Update, interval: int = 60,) -> int:
    logging.info("NO CONVERT TO seconds")
    if "hora" in update.message.text:
        return float(str(update.message.text).split(" ")[0]) * 60 * 60
    if "minuto" in update.message.text:
        return float(str(update.message.text).split(" ")[0]) * 60


async def validate_choices(reply: str, text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Valida qual dos textos exibir, mostrando escolhas 
        pré-definas, ou liberando a escrita
    """
    if text.lower() == "ano" or text.lower() == "quilometragem":
        new_reply = REPLY_DEFAULT + f" para {text.lower()} (números apenas): "
        try:
            await update.message.reply_text(new_reply)
        except Exception as e:
            show_error(update, context)
            return ConversationHandler.END
    elif text.lower() == "direção":
        try:
            await update.message.reply_text(reply, reply_markup=strwheel_markup)
        except Exception as e:
            show_error(update, context)
            return ConversationHandler.END
    elif "combustível" in text.lower():
        try:
            await update.message.reply_text(reply, reply_markup=gas_markup)
        except Exception as e:
            show_error(update, context)
            return ConversationHandler.END
    elif "câmbio" in text.lower():
        try:
            await update.message.reply_text(reply, reply_markup=gear_markup)
        except Exception as e:
            show_error(update, context)
            return ConversationHandler.END
    else:
        try:
            await update.message.reply_text(reply)
        except Exception as e:
            show_error(update, context)
            return ConversationHandler.END


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Cria o loop das notificações
    """
    interval = _convert_to_seconds(update)
    logging.info(f"INTERVAL {interval}")
    stop_timer = False
    start_time = time.perf_counter()
    try:
        if interval < 0:
            await update.effective_message.reply_text("Intervalo inválido!")
        await update.effective_message.reply_text(
            f"Beleza! Intervalo de {interval} segundos configurado!")
        while not stop_timer:
            elapsed_time = time.perf_counter() - start_time
            if elapsed_time >= interval:
                await alarm(interval, update)
                start_time = time.perf_counter()
                stop_timer = await unset_timer(update, context)
            # verificar a variável de controle

    except Exception as e:
        logging.info(e)
        await update.effective_message.reply_text("Ops! houve um erro, tente novamente!")
        return ConversationHandler.END


async def unset_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "unset" in update.message.text:
        await update.effective_message.reply_text("Beleza! Intervalo removido!")
        return True


async def show_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Mostra uma mensagem de erro padrão
    """
    await update.message.reply_text(
        "Ocorreu um erro inesperado!\n" +
        "Por favor, tente novamente com o comando /start \n" +
        "ou veja a lista de comandos com o comando /help.\n"
    )
