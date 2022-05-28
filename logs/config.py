from datetime import datetime

from bases import NamedSingleton


class Logger(metaclass=NamedSingleton):
    """
    The main config class for a simple logger.
    """

    def __init__(self, logger_name: str):
        """
        Initialization of the logger.

        :param logger_name: filename
        """
        self.name = logger_name

    def logger(self, message: str):
        """
        Main logging class.
        Opens the log file and appends the message there.

        :param message: logging message
        """
        with open(f'logs/{self.name}.log', 'a') as file:
            message = f'Date: {datetime.now().replace(microsecond=0)}\n' \
                    + message + '\n'
            file.write(message)
            file.close()
