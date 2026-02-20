from src.repository.repo_memory import *
from src.repository.repo_text import *
from src.repository.repo_binary import *
from src.services.undo_service import *


class StudentService:
    def __init__(self, repo, undo_service):
        self._repo = repo
        self._undo_service = undo_service
        # self._data = self._repo.data()

    def add(self, student: Student):
        try:
            self._repo.add(student)
            undo_func = FunctionCall(self.remove, student.id)
            redo_func = FunctionCall(self.add, student)
            self._undo_service.record(Operation(undo_func, redo_func))
        except InvalidNameError:
            raise InvalidNameError
        except DuplicateIDError:
            raise DuplicateIDError

    def remove(self, student_id: int):
        try:
            student = self._repo.remove(student_id)
            last_undo: CascadedOperation = self._undo_service.pop_operation() # this last undo is a CascadedOperation
            undo_func = FunctionCall(self.add, student)
            redo_func = FunctionCall(self.remove, student.id)
            last_undo.add_undo_function(undo_func)
            last_undo.add_redo_function(redo_func)
            self._undo_service.record(Operation(undo_func, redo_func))
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_id(self, stud_id: int) -> Student:
        try:
            student = self._repo.find_id(stud_id)
            return student
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_name(self, student_name: str) -> list:
        try:
            lst = self._repo.find_name(student_name)
            return lst
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except NameNotFoundError:
            raise NameNotFoundError

    def update_name(self, new_name: str, student_id: int):
        try:
            student = self._repo.find_id(student_id)
            self._repo.update_name(new_name, student_id)
            undo_func = FunctionCall(self.update_name, student.name, student.id)
            redo_func = FunctionCall(self.update_name, new_name, student.id)
            self._undo_service.record(Operation(undo_func, redo_func))
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except IDNotFoundError:
            raise IDNotFoundError

    def get_all(self) -> dict:
        return self._repo.data

    def load(self):
        try:
            self._repo.load()
        except AttributeError:
            raise AttributeError

    # def data(self):
    #     return self._data


