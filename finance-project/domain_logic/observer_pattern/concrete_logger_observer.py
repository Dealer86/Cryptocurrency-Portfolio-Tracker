from domain_logic.observer_pattern.observer import Observer

import logging


class ConcreteLoggerObserver(Observer):
    def update(self, message: str):
        logging.info(message)
