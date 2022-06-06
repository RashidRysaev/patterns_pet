from datetime import datetime

from bases import NamedSingleton, LoggerStrategy


class ConsoleLogger(LoggerStrategy):
     def __init__(self, name):
         self.name = name

     def write(self, text):
         message = f'Date: {datetime.now().replace(microsecond=0)}\n' \
                   + text + '\n'
         print(message)


class FileLogger(LoggerStrategy):
    def __init__(self, filename):
        self.filename = filename

    def write(self, text):
        with open(f'logs/{self.filename}.log', 'a', encoding='utf-8') as file:
            message = f'Date: {datetime.now().replace(microsecond=0)}\n' \
                    + text + '\n'
            file.write(message)
            file.close()


class Logger(metaclass=NamedSingleton):
    """
    The main config class for a simple logger.
    """
    
    strategies = {
         'console': ConsoleLogger,
         'file': FileLogger
    }

    def __init__(self, logger_name, logger_type):
        """
        Initialization of the logger.

        :param logger_name: filename
        """
        self.name = logger_name
        self.log_strategy = self.strategies[logger_type](self.name)

    def logger(self, message):
        """
        Main logging class.
        Opens the log file and appends the message there.

        :param message: logging message
        """
        self.log_strategy.write(message)
