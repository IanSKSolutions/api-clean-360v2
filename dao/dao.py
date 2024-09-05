from abc import ABC, abstractmethod

class DAO(ABC):
    @abstractmethod
    def list(self, month, year):
        pass