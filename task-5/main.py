# Task 5 (Observable/EventEmitter/Alternative) -- Reactive message based communication between entities

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class Observable(ABC):
    def __init__(self) -> None:
        self.observers: List[Observer]= []

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def notify(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)


class User(Observable):
    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        self.username: str = username
        self._password: str = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        now = datetime.now()
        self.notify(self.username, now)


class UserLogger(Observer):
    def update(self, username: str, when: datetime):
        when_fmt = when.strftime("%d.%m.%Y %H:%M:%S") 
        print(f"User '{username}' changed their password at {when_fmt}.")


def main():
    john = User("johndoe", "pass")
    logger = UserLogger()
    john.attach(logger)
    john.password = "#E2aWW@4v%2^&P&S"

if __name__ == "__main__":
    main()
