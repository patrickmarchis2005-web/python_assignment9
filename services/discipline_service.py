from src.repository.repo_memory import *
from src.repository.repo_text import *
from src.repository.repo_binary import *
from src.services.undo_service import *


class DisciplineService:
    def __init__(self, repo, undo_service):
        self._repo = repo
        self._undo_service = undo_service
        self._data = self._repo.data

    def add(self, discipline: Discipline):
        try:
            self._repo.add(discipline)
            undo_func = FunctionCall(self.remove, discipline.id)
            redo_func = FunctionCall(self.add, discipline)
            self._undo_service.record(Operation(undo_func, redo_func))
        except InvalidNameError:
            raise InvalidNameError
        except DuplicateIDError:
            raise DuplicateIDError

    def remove(self, discipline_id: int):
        try:
            discipline = self._repo.remove(discipline_id)
            undo_func = FunctionCall(self.add, discipline)
            redo_func = FunctionCall(self.remove, discipline_id)
            self._undo_service.record(Operation(undo_func, redo_func))
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_id(self, discipline_id: int):
        try:
            discipline = self._repo.find_id(discipline_id)
            return discipline
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_name(self, discipline_name: str) -> list:
        try:
            list_disciplines = self._repo.find_name(discipline_name)
            return list_disciplines
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except NameNotFoundError:
            raise NameNotFoundError

    def update_name(self, new_name: str, discipline_id: int):
        try:
            discipline = self._repo.find_id(discipline_id)
            self._repo.update_name(new_name, discipline_id)
            undo_func = FunctionCall(self.update_name, discipline.name, discipline_id)
            redo_func = FunctionCall(self.update_name, new_name, discipline_id)
            self._undo_service.record(Operation(undo_func, redo_func))
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except IDNotFoundError:
            raise IDNotFoundError

    def get_all(self):
        return self._repo.data

    def load(self):
        try:
            self._repo.load()
        except AttributeError:
            raise AttributeError

    def data(self):
        return self._data


