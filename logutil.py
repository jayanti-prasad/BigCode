import sys
import logging
import logging.handlers
import os


def get_logger(logger_name, log_dir, log_file, log_level='DEBUG', log_to_console=True):
    root_logger = logging.getLogger(logger_name)
    root_logger.setLevel(log_level)
    handler = logging.handlers.RotatingFileHandler(log_dir + os.sep + log_file, maxBytes=10000000, backupCount=10,
                                                   encoding='utf-8')
    formatter = logging.Formatter('%(name)s - %(asctime)s -%(levelname)s - %(message)s')
    handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
    root_logger.addHandler(handler)
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    return root_logger
