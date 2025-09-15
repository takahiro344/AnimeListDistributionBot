from abc import ABC, abstractmethod


class UserRepositoryInterface(ABC):
    @abstractmethod
    def add(self, user_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
