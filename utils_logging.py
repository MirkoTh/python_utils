import logging

def conf_logger(lg_name = False, level = logging.INFO):
    """ This function initializes a logger logging in the output of the main script """
    logger = logging.getLogger(lg_name)
    logger.setLevel(level)
    # create handler
    handler = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return(logger)