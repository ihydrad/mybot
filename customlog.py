import os
import logging
import logging.handlers
from os.path import exists
import api.config as config


formatter = logging.Formatter(
                            '%(asctime)s %(levelname)s[%(name)s]:%(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S')


class LoggerConsole:
    def __init__(self, name) -> None:
        self.logger = logging.getLogger(name.lower())
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(lev)
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(consoleHandler)
        self.logger.info("Init logger")


class LoggerFile:
    def __init__(self, name) -> None:
        self.logger = logging.getLogger(name.lower())
        log_file = os.path.join(config.work_dir, "logs", name.lower() + '.log')
        log_folder = os.path.join(config.work_dir, "logs")

        if not exists(log_folder):
            os.mkdir(log_folder)

        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.info("Init logger")
