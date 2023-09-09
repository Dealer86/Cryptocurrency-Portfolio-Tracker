from abc import ABC, abstractmethod

from domain_logic.logging.observer import Observer


class Subject(ABC):
    @abstractmethod
    def add_observer(self, o: Observer):
        pass

    @abstractmethod
    def remove_observer(self, o: Observer):
        pass

    @abstractmethod
    def notify_observer(self, message: str):
        pass
