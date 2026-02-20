import pickle
from symbol import raise_stmt

from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.domain.student import Student
from src.repository.repo_memory import StudentMemoryRepo, RepositoryError, DisciplineMemoryRepo, GradeMemoryRepo, \
    DuplicateIDError, IDNotFoundError, NameNotFoundError, GradeNotFoundError, InvalidNameError, InvalidGradeError, \
    EmptyRepositoryError, DuplicateNameError


class StudentBinRepo(StudentMemoryRepo):
    def __init__(self, file_name: str = "students.pickle"):
        super().__init__()
        self.__file_name = file_name
        self.load()

    def load(self):
        try:
            fin = open(self.__file_name, 'rb')
            self.erase_all()
            self._data = pickle.load(fin)
            fin.close()
        except FileNotFoundError:
            pass
        except EOFError:
            pass

    def save(self):
        try:
            fout = open(self.__file_name, "wb")
        except FileNotFoundError:
            raise RepositoryError("\nThe specified binary file was not found\n")
        except Exception:
            raise RepositoryError("\nSomething went wrong\n")
        pickle.dump(self._data, fout)
        fout.close()

    def add(self, student: Student):
        try:
            super().add(student)
            self.save()
        except InvalidNameError:
            raise InvalidNameError()
        except DuplicateIDError:
            raise DuplicateIDError()

    def remove(self, student_id: int):
        try:
            student = super().remove(student_id)
            self.save()
            return student
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def find_id(self, stud_id: int) -> Student:
        try:
            student = super().find_id(stud_id)
            return student
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def find_name(self, discipline_name: str) -> list:
        try:
            lst = super().find_name(discipline_name)
            return lst
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except InvalidNameError:
            raise InvalidNameError()
        except NameNotFoundError:
            raise NameNotFoundError()

    def update_name(self, new_name: str, student_id: int):
        try:
            super().update_name(new_name=new_name, student_id=student_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except InvalidNameError:
            raise InvalidNameError()
        except IDNotFoundError:
            raise IDNotFoundError()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data


class DisciplineBinRepo(DisciplineMemoryRepo):
    def __init__(self, file_name: str = "disciplines.pickle"):
        super().__init__()
        self.__file_name = file_name
        self.load()

    def load(self):
        try:
            fin = open(self.__file_name, 'rb')
            self.erase_all()
            self._data = pickle.load(fin)
            fin.close()
        except FileNotFoundError:
            pass
        except EOFError:
            pass

    def save(self):
        try:
            fout = open(self.__file_name, "wb")
        except FileNotFoundError:
            raise RepositoryError("\nThe specified binary file was not found\n")
        except Exception:
            raise RepositoryError("\nSomething went wrong\n")
        pickle.dump(self._data, fout)
        fout.close()

    def add(self, discipline: Discipline):
        try:
            super().add(discipline)
            self.save()
        except DuplicateNameError:
            raise DuplicateNameError()
        except InvalidNameError:
            raise InvalidNameError()
        except DuplicateIDError:
            raise DuplicateIDError()

    def remove(self, discipline_id: int):
        try:
            discipline = super().remove(discipline_id)
            self.save()
            return discipline
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def find_id(self, discipline_id: int) -> Discipline:
        try:
            discipline = super().find_id(discipline_id)
            return discipline
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def find_name(self, discipline_name: str) -> Discipline:
        try:
            list_disciplines = super().find_name(discipline_name)
            return list_disciplines
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except InvalidNameError:
            raise InvalidNameError()
        except NameNotFoundError:
            raise NameNotFoundError()

    def update_name(self, new_name: str, discipline_id: int):
        try:
            super().update_name(new_name, discipline_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except InvalidNameError:
            raise InvalidNameError()
        except IDNotFoundError:
            raise IDNotFoundError()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data


class GradeBinRepo(GradeMemoryRepo):
    def __init__(self, stud_memo_repo: StudentMemoryRepo, disc_memo_repo: DisciplineMemoryRepo, file_name: str = "grades.pickle"):
        super().__init__(stud_memo_repo, disc_memo_repo)
        self.__file_name = file_name
        self.load()

    def load(self):
        try:
            fin = open(self.__file_name, 'rb')
            self.erase_all()
            self._data = pickle.load(fin)
            fin.close()
        except FileNotFoundError:
            pass
        except EOFError:
            pass

    def save(self):
        try:
            fout = open(self.__file_name, "wb")
        except FileNotFoundError:
            raise RepositoryError("\nThe specified binary file was not found\n")
        except Exception:
            raise RepositoryError("\nSomething went wrong\n")
        pickle.dump(self._data, fout)
        fout.close()

    def add(self, grade: Grade):
        try:
            super().add(grade)
            self.save()
        except InvalidGradeError:
            raise InvalidGradeError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def remove_discipline(self, discipline_id: int):
        try:
            super().remove_discipline(discipline_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def remove_student(self, student_id: int):
        try:
            super().remove_student(student_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()

    def remove_grade(self, student_grade: Grade):
        try:
            super().remove_grade(student_grade)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError()
        except GradeNotFoundError:
            raise GradeNotFoundError()

    def find_grades(self, stud_id: int, discipline_id: int) -> list:
        try:
            lst: list = super().find_grades(stud_id, discipline_id)
            return lst
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()


    def update_grade(self, new_grade: int, actual_grade: Grade):
        try:
            super().update_grade(new_grade, actual_grade)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except InvalidGradeError:
            raise InvalidGradeError()
        except IDNotFoundError:
            raise IDNotFoundError()
        except GradeNotFoundError:
            raise GradeNotFoundError()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data

