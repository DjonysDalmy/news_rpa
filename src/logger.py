import logging

class Logger:
    _logger = None

    @staticmethod
    def setup():
        if Logger._logger is None:
            Logger._logger = logging.getLogger('NewsRobotLogger')
            Logger._logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            Logger._logger.addHandler(handler)

    @staticmethod
    def info(message):
        if Logger._logger is not None:
            Logger._logger.info(message)

    @staticmethod
    def error(message):
        if Logger._logger is not None:
            Logger._logger.error(message)

    @staticmethod
    def warning(message):
        if Logger._logger is not None:
            Logger._logger.warning(message)

    @staticmethod
    def debug(message):
        if Logger._logger is not None:
            Logger._logger.debug(message)

    @staticmethod
    def critical(message):
        if Logger._logger is not None:
            Logger._logger.critical(message)
