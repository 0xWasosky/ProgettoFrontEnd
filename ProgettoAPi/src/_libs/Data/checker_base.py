from abc import ABC, abstractmethod


class IChecker(ABC):
    @staticmethod
    @abstractmethod
    def check():
        pass
