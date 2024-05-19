from abc import ABC, abstractmethod


class StoreInterface(ABC):
    @abstractmethod
    def switch_to(self, project: str):
        ...

    @abstractmethod
    def get_total_spent_per_project(self):
        ...

    @abstractmethod
    def get_current_project(self) -> str:
        ...
