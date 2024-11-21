from abc import ABC, abstractmethod

class IHandler(ABC):
    @abstractmethod
    def handle(self, request):
        pass