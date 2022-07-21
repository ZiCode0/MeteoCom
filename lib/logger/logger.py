from loguru import logger


# from lib import notify


def init_logger(program_name, log_level='DEBUG'):
    """
    Logger for program
    :type program_name: name of current program
    :type log_level: log level to filter output
    logger call example:
     - INFO: logger.info( TEXT )
     - WARNING:: logger.warning( TEXT )
     -
    """
    # set log format
    logger.add('{program_name}.log'.format(program_name=program_name),
               format='{time:!UTC} {level} {message}',
               level=log_level,
               rotation='1 MB',
               compression='zip')
