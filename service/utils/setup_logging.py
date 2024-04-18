import logging

from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

def setup_logging(logs_output_file):
    
    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)

    # format logs as json
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        rename_fields={"asctime": "@timestamp", "levelname": "level"},
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )

    # add logs to file
    file_log_handler = RotatingFileHandler(logs_output_file, maxBytes=10*1024*1024, backupCount=1)
    file_log_handler.setFormatter(json_formatter)
    logger.addHandler(file_log_handler)

    # add logs to console
    console_log_handler = logging.StreamHandler()
    console_log_handler.setFormatter(json_formatter)
    logger.addHandler(console_log_handler)


def get_logger(logger_name, extra):
    logger = logging.LoggerAdapter(
        logging.getLogger(logger_name),
        extra=extra
    )
    
    return logger





