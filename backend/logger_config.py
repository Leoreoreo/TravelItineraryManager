import logging
from colorlog import ColoredFormatter

def get_logger(name: str):
    # Define a custom formatter with colors
    log_format = "%(log_color)s[%(asctime)s] %(levelname)s: %(message)s"
    color_formatter = ColoredFormatter(
        log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    # Set up a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the desired log level
    logger.addHandler(console_handler)

    return logger

