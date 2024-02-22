import logging
from logging.handlers import TimedRotatingFileHandler


class CustomLogger(logging.Logger):
    """Custom logger to add user_email to log messages"""

    user_email = None

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.user_email = None

    def update_user_email(self, user_email):
        self.user_email = user_email

    def _log(self, level, msg, args, **kwargs):
        if self.user_email:
            msg = f"{self.user_email}: {msg}"
        super()._log(level, msg, args, **kwargs)

class CustomFormatter(logging.Formatter):
    """Custom logging format with emojis"""
    level_formats = {
        logging.DEBUG: "🐞",
        logging.INFO: "👾",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "🔥",
        logging.FATAL: "💀",
    }

    # Override the format method to include the emoji
    def format(self, record):
        record.message = record.getMessage()
        formatted_line = f"{self.formatTime(record, self.datefmt)}- {self.level_formats.get(record.levelno, '')} {record.message}"
        return formatted_line
    

def setup_logging():
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.__class__ = CustomLogger

    # Define the log file name
    log_file = "logs/log"

    # Create timed rotating file handler
    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Set the CustomFormatter for the file handler
    custom_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_handler.setFormatter(CustomFormatter(custom_format))

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Create console handler for logging to the console with the same CustomFormatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(CustomFormatter(custom_format))
    
    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # To prevent log messages from being duplicated in the console,
    # disable propagation for the logger
    logger.propagate = False

def get_logger():
    logger = logging.getLogger(__name__)
    return logger