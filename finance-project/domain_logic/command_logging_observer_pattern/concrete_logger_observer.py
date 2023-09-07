from domain_logic.command_logging_observer_pattern.observer import Observer

import logging


class ConcreteLoggerObserver(Observer):
    def update(self, message: str):
        logging.info(message)
