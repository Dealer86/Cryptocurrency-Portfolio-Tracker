from abc import ABC, abstractmethod


class Subject(ABC):
    @abstractmethod
    def add_observer(self, o):
        pass

    @abstractmethod
    def remove_observer(self, o):
        pass

    @abstractmethod
    def notify_observer(self, message: str):
        pass
