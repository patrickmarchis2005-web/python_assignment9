from src.repository.repo_memory import StudentMemoryRepo, DisciplineMemoryRepo, GradeMemoryRepo, NameNotFoundError, \
    IDNotFoundError, GradeNotFoundError, EmptyRepositoryError, DuplicateNameError
from src.domain.discipline import Discipline
from src.domain.student import Student
from src.domain.grade import Grade
from src.repository.repo_memory import RepositoryError, DuplicateIDError, InvalidNameError, InvalidGradeError


class StudentFileRepo(StudentMemoryRepo):
    def __init__(self, file_name: str = "students.txt"):
        super().__init__()
        self.__file_name = file_name
        self.load()

    def load(self):
        try:
            fin = open(self.__file_name, 'rt', encoding="utf-8")
            self.erase_all()
            lines = fin.readlines()
            for line in lines:
                current_line = line.split(",")
                new_student = Student(int(current_line[0]), current_line[1])
                super().add(new_student)
            fin.close()
        except FileNotFoundError:
            pass

    def save(self):
        try:
            fout = open(self.__file_name, 'wt', encoding="utf-8")
        except FileNotFoundError:
            raise RepositoryError("\nThe specified file was not found\n")
        except Exception:
            raise RepositoryError("\nSomething went wrong\n")
        for student in self._data.values():
            student_str = str(student.id) + "," + str(student.name) + "\n"
            fout.write(student_str)
        fout.close()

    def add(self, student: Student):
        try:
            super().add(student)
            self.save()
        except InvalidNameError:
            raise InvalidNameError
        except DuplicateIDError:
            raise DuplicateIDError

    def remove(self, student_id: int):
        try:
            student = super().remove(student_id)
            self.save()
            return student
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_id(self, stud_id: int) -> Student:
        try:
            student = super().find_id(stud_id)
            return student
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_name(self, discipline_name: str) -> list:
        try:
            lst = super().find_name(discipline_name)
            return lst
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except NameNotFoundError:
            raise NameNotFoundError

    def update_name(self, student_id: int, name: str):
        try:
            super().update_name(name, student_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except IDNotFoundError:
            raise IDNotFoundError

    def erase_all(self):
        super().erase_all()
        # self.save()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data


class DisciplineFileRepo(DisciplineMemoryRepo):
    def __init__(self, file_name: str = "disciplines.txt"):
        super().__init__()
        self.__file_name = file_name
        self.load()

    def load(self):
        try:
            fin = open(self.__file_name, 'rt')
            self.erase_all()
            lines = fin.readlines()
            for line in lines:
                current_line = line.split(",")
                new_discipline = Discipline(int(current_line[0]), current_line[1])
                super().add(new_discipline)
            fin.close()
        except FileNotFoundError:
            pass

    def save(self):
        try:
            fout = open(self.__file_name, 'wt', encoding="utf-8")
        except FileNotFoundError:
            raise RepositoryError("\nThe specified file was not found\n")
        except Exception:
            raise RepositoryError("\nSomething went wrong\n")
        for discipline in self._data.values():
            discipline_str = str(discipline.id) + "," + discipline.name + "\n"
            fout.write(discipline_str)
        fout.close()

    def add(self, discipline: Discipline):
        try:
            super().add(discipline)
            self.save()
        except DuplicateNameError:
            raise DuplicateNameError
        except InvalidNameError:
            raise InvalidNameError
        except DuplicateIDError:
            raise DuplicateIDError

    def remove(self, discipline_id: int):
        try:
            discipline = super().remove(discipline_id)
            self.save()
            return discipline
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_id(self, discipline_id: int) -> Discipline:
        try:
            discipline = super().find_id(discipline_id)
            return discipline
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def find_name(self, discipline_name: str) -> Discipline:
        try:
            list_disciplines = super().find_name(discipline_name)
            return list_disciplines
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except NameNotFoundError:
            raise NameNotFoundError

    def update_name(self, discipline_id: int, name: str):
        try:
            super().update_name(name, discipline_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidNameError:
            raise InvalidNameError
        except IDNotFoundError:
            raise IDNotFoundError

    def erase_all(self):
        super().erase_all()
        # self.save()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data


class GradeFileRepo(GradeMemoryRepo):
    def __init__(self, student_memo_repo: StudentMemoryRepo, discipline_memo_repo: DisciplineMemoryRepo, file_name: str = "grades.txt"):
        super().__init__(student_memo_repo, discipline_memo_repo)
        self.__file_name = file_name
        self.load()

    def load(self):
        try:
            fin = open(self.__file_name, 'rt')
            self.erase_all()
            lines = fin.readlines()
            for line in lines:
                halves = line.split(":")
                ids = halves[0].split(",")
                values = halves[1].split(",")
                for i in range(len(values)):
                    new_grade = Grade(int(ids[0]), int(ids[1]), int(values[i]))
                    super().add(new_grade)
            fin.close()
        except FileNotFoundError:
            pass

    def save(self):
        try:
            fout = open(self.__file_name, 'wt', encoding="utf-8")
        except FileNotFoundError:
            raise RepositoryError("\nThe specified file was not found\n")
        except Exception:
            raise RepositoryError("\nSomething went wrong\n")
        for key in self._data.keys():
            stud_id = key[0]
            disc_id = key[1]
            # grades = self._data[key]
            grades = ",".join(map(str, self._data[key]))
            represent = str(stud_id) + "," + str(disc_id) + ":" + grades + "\n"
            fout.write(represent)
        fout.close()

    def add(self, grade: Grade):
        try:
            super().add(grade)
            self.save()
        except InvalidGradeError:
            raise InvalidGradeError
        except IDNotFoundError:
            raise IDNotFoundError

    def remove_discipline(self, discipline_id: int):
        try:
            super().remove_discipline(discipline_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def remove_student(self, student_id: int):
        try:
            super().remove_student(student_id)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def remove_grade(self, student_grade: Grade):
        try:
            super().remove_grade(student_grade)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError
        except GradeNotFoundError:
            raise GradeNotFoundError

    def find_grades(self, stud_id: int, discipline_id: int) -> list:
        try:
            lst: list = super().find_grades(stud_id, discipline_id)
            return lst
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except IDNotFoundError:
            raise IDNotFoundError

    def update_grade(self, new_grade: int, actual_grade: Grade):
        try:
            super().update_grade(new_grade, actual_grade)
            self.save()
        except EmptyRepositoryError:
            raise EmptyRepositoryError
        except InvalidGradeError:
            raise InvalidGradeError
        except IDNotFoundError:
            raise IDNotFoundError
        except GradeNotFoundError:
            raise GradeNotFoundError

    def erase_all(self):
        super().erase_all()
        # self.save()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data

