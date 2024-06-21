from voe.config import Settings
from voe.app import Application


def run():
    """Run VOE disconnect status application"""
    app = Application(settings=Settings())
    app.notify_in_telegram()


if __name__ == '__main__':
    run()
