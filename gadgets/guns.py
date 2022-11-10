from abc import ABC, abstractmethod


class Gun(ABC):
    delay = 0

    @abstractmethod
    def fire(self):
        pass
