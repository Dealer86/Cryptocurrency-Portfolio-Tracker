from domain_logic.logging.observer import Observer

import logging


class ConcreteLoggerObserver(Observer):
    def update(self, message: str):
        logging.info(message)
