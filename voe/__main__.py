from voe.config import Settings
from voe.app import Application
from voe.logger import logger_configure


def run():
    """Run VOE disconnect status application"""
    settings = Settings()

    logger_configure(
        level=settings.LOG_LEVEL,
        root_level=settings.LOG_ROOT_LEVEL,
    )
    app = Application(settings=settings)
    app.notify_in_telegram()


if __name__ == '__main__':
    run()
