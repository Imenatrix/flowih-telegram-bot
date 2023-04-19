
from factories.app_factory import AppFactory


def main() -> None:
    """Roda o bot"""
    app = AppFactory()
    app.run()    




if __name__ == "__main__":
    main()