from src.repository.repo_memory import *
from src.repository.repo_text import *
from src.repository.repo_binary import *
from src.services.undo_service import FunctionCall, Operation, CascadedOperation


class GradeService:
    def __init__(self, repo, undo_service):
        self._repo = repo
        self._undo_service = undo_service
        self._data = self._repo.data

    def add(self, grade: Grade):
        try:
            self._repo.add(grade)
            undo_func = FunctionCall(self.remove_grade, grade)
            redo_func = FunctionCall(self.add, grade)
            self._undo_service.record(Operation(undo_func, redo_func))
        except InvalidGradeError:
            raise InvalidGradeError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def remove_discipline(self, discipline_id: int):
        try:
            cascade = CascadedOperation()
            catalog: dict = self._repo.data

            for key in catalog.keys():
                if key[1] == discipline_id:
                    for value in catalog[key]:
                        grade = Grade(key[0], discipline_id, value)
                        undo_func = FunctionCall(self.add, grade)
                        cascade.add_undo_function(undo_func)
                        self.remove_grade(grade)
            redo_func = FunctionCall(self.remove_discipline, discipline_id)
            cascade.add_redo_function(redo_func)
            self._undo_service.record(cascade)
            self._repo.remove_discipline(discipline_id)
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def remove_student(self, student_id: int):
        try:
            cascade = CascadedOperation()
            catalog: dict = self._repo.data

            for key in catalog.keys():
                if key[0] == student_id:
                    for value in catalog[key]:
                        grade = Grade(student_id, key[1], value)
                        undo_func = FunctionCall(self.add, grade)
                        cascade.add_undo_function(undo_func)
                        self.remove_grade(grade)
            redo_func = FunctionCall(self.remove_student, student_id)
            cascade.add_redo_function(redo_func)
            self._undo_service.record(cascade)
            self._repo.remove_student(student_id)
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def remove_grade(self, student_grade: Grade):
        try:
            undo_func = FunctionCall(self.add, student_grade)
            redo_func = FunctionCall(self.remove_grade, student_grade)
            self._undo_service.record(Operation(undo_func, redo_func))
            self._repo.remove_grade(student_grade)
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidGradeError:
            raise InvalidGradeError
        except IDNotFoundError:
            raise IDNotFoundError
        except GradeNotFoundError:
            raise GradeNotFoundError

    def find_grades(self, stud_id: int, discipline_id: int) -> list:
        try:
            lst = self._repo.find_grades(stud_id, discipline_id)
            return lst
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def update_grade(self, new_grade: int, actual_grade: Grade):
        try:
            undo_func = FunctionCall(self.update_grade, actual_grade.grade_value, actual_grade)
            redo_func = FunctionCall(self.update_grade, new_grade, actual_grade)
            self._undo_service.record(Operation(undo_func, redo_func))
            self._repo.update_grade(new_grade, actual_grade)
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except InvalidGradeError:
            raise InvalidGradeError()
        except IDNotFoundError:
            raise IDNotFoundError()
        except GradeNotFoundError:
            raise GradeNotFoundError()

    def get_all(self):
        return self._repo.data

    def load(self):
        try:
            self._repo.load()
        except AttributeError:
            raise AttributeError

    def data(self):
        return self._data


