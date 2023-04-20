import asyncio
import time
import logging
from typing import Dict
from datetime import datetime
from telegram import ReplyKeyboardRemove, Update
from settings import (
    TYPING_REPLY,
    CHOOSING,
    TIMER,
    REPLY_DEFAULT,
    user_info,
    current_interval,
    current_process,
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

user_info = {
    "interval": 0
}


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
        show_error(update, context, e)
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
    user_info = {key.lower().replace(" ", "_"): value for key,
                 value in user_data.items()}
    print(user_info)
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


async def show_help(update: Update) -> None:
    await update.effective_message.reply_text(
        "Comandos aceitos:\n" +
        "- /start: Começa o fluxo\n" +
        "- /help: Mostra comandos\n" +
        "- /unset: Remove intervalo configurado\n"
    )


def _convert_to_seconds(update: Update, interval: int = 60,) -> int:
    if "hora" in update.message.text:
        return float(str(update.message.text).split(" ")[0]) * 60 * 60
    if "minuto" in update.message.text:
        return float(str(update.message.text).split(" ")[0]) * 60


async def validate_choices(reply: str, text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Valida qual dos textos exibir, mostrando escolhas
        pré-definas, ou liberando a escrita
    """
    logging.info(f"validate choices - {text.lower()}")
    if text.lower() == "ano" or text.lower() == "quilometragem":
        new_reply = REPLY_DEFAULT + f" para {text.lower()} (números apenas): "
        try:
            await update.message.reply_text(new_reply)
        except Exception as e:
            await show_error(update, context, e)
            return ConversationHandler.END
    elif text.lower() == "direção":
        try:
            await update.message.reply_text(reply, reply_markup=strwheel_markup)
        except Exception as e:
            await show_error(update, context, e)
            return ConversationHandler.END
    elif "combustível" in text.lower():
        try:
            await update.message.reply_text(reply, reply_markup=gas_markup)
        except Exception as e:
            await show_error(update, context, e)
            return ConversationHandler.END
    elif "câmbio" in text.lower():
        try:
            await update.message.reply_text(reply, reply_markup=gear_markup)
        except Exception as e:
            await show_error(update, context, e)
            return ConversationHandler.END
    else:
        try:
            await update.message.reply_text(reply)
        except Exception as e:
            await show_error(update, context, e)
            return ConversationHandler.END


async def set_client_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Cria o loop das notificações
    """
    current_interval = _convert_to_seconds(update)
    logging.info(f"INTERVAL {current_interval}")
    user_info["interval"] = current_interval
    try:
        if current_interval <= 0:
            await update.effective_message.reply_text("Intervalo inválido!")
        await update.effective_message.reply_text(
            f"Beleza! Intervalo de {current_interval} segundos configurado!")
        # TODO: Salvar intervalo no banco
    except Exception as e:
        logging.info(e)
        await update.effective_message.reply_text("Ops! houve um erro, tente novamente!")
        return ConversationHandler.END


def alarm(update: Update) -> None:
    """
        Manda a notificação.
    """
    logging.info(f"NO ALARM  {current_interval}")
    update.effective_message.reply_text(
        f"{current_interval} segundos passaram! Aeee!")


def get_time(start_time, update: Update):
    '''
        Especifica a prioridade e o intervalo de cada scheduler, 
        a partir do intervalo posto pelo user.

        Se o user ainda não tiver preenchido,
        usa 60 seg como padrão e não chama o alarm.
    '''
    print(f"Tempo {datetime.now().strftime('%H:%M:%S')}")
    elapsed_time = time.perf_counter() - start_time

    if user_info["interval"]:
        logging.info(f"NO IF {user_info['interval'] }")
        if int(elapsed_time) == int(user_info["interval"]):
            alarm(update)
        time.sleep(user_info["interval"])
        get_time(start_time, update)
    else:
        logging.info(f"NO ELSE {user_info['interval'] }")
        start_time = time.perf_counter()
        time.sleep(60)
        get_time(start_time, update)
        alarm(user_info["interval"], update)


async def unset_client_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Remove o intervalo salvo no banco
    """
    if "unset" in update.message.text:
        if current_process != None:
            current_process.kill()
        # TODO: remover intervalo do banco
        await update.effective_message.reply_text("Beleza! Intervalo removido!")


async def show_error(update: Update, context: ContextTypes.DEFAULT_TYPE, e: Exception) -> None:
    """
        Mostra uma mensagem de erro padrão
    """
    logging.info(e)
    await update.message.reply_text(
        "Ocorreu um erro inesperado!\n" +
        "Por favor, tente novamente com o comando /start \n" +
        "ou veja a lista de comandos com o comando /help.\n"
    )


def unset_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if current_process != None:
        current_process.kill()
