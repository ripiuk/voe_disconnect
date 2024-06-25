import sys
import logging


LOG_BASE_NAME = 'voe'
LOG_FORMAT = '%(asctime)s %(levelname)-7s %(name)-15s: %(message)s'
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def logger_configure(*, level: str = 'DEBUG', root_level: str = 'WARNING') -> None:
    """Configure console logger."""
    log_handler = logging.StreamHandler(stream=sys.stdout)

    log_formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    log_handler.setFormatter(log_formatter)

    # root logger
    logging.getLogger('').addHandler(log_handler)
    logging.getLogger('').setLevel(root_level)

    # local logger
    logging.getLogger(LOG_BASE_NAME).setLevel(level)
