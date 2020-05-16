import os.path
import logging
import logging.config


def initialize_logger():
    """

    :return: logger object
    """
    log_file = os.path.dirname(__file__) + '/../utils/log.conf'
    logging.config.fileConfig(fname=log_file, disable_existing_loggers=False)
    return logging
