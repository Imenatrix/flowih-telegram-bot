import logging
import bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Roda o bot"""
    bot.init()


if __name__ == "__main__":
    main()
