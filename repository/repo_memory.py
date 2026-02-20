from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.domain.student import Student
from faker import Faker
from random import randint, randrange


class RepositoryError(Exception):
    def __init__(self, message: str = ""):
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message


class DuplicateIDError(RepositoryError):
    def __init__(self):
        super().__init__("\nDuplicate ID\n")


class IDNotFoundError(RepositoryError):
    def __init__(self):
        super().__init__("\nID not found\n")


class NameNotFoundError(RepositoryError):
    def __init__(self):
        super().__init__("\nName not found\n")


class InvalidNameError(RepositoryError):
    def __init__(self):
        super().__init__("\nInvalid name\n")


class DuplicateNameError(RepositoryError):
    def __init__(self):
        super().__init__("\nDuplicate name\n")


class GradeNotFoundError(RepositoryError):
    def __init__(self):
        super().__init__("\nGrade not found\n")


class InvalidGradeError(RepositoryError):
    def __init__(self):
        super().__init__("\nInvalid grade\n")


class EmptyRepositoryError(RepositoryError):
    def __init__(self):
        super().__init__("\nEmpty repository\n")


class RepositoryIterator:
    def __init__(self, data):
        self.__data = data
        self.__pos = -1

    def __next__(self):
        self.__pos += 1
        if len(self.__data) == self.__pos:
            raise StopIteration
        return self.__data[self.__pos]


def random_students() -> dict:
    fake = Faker("ro_RO")
    data: dict = {}
    for i in range(20):
        while True:
            id = randint(100, 200)
            if id not in data.keys():
                break
        student_name = fake.name().upper()
        student = Student(id, student_name)
        data[id] = student
    return data


def random_discipline() -> dict:
    data: dict = {}
    elements = ["ASC", "FP", "C-LOGIC", "ALGEBRA", "MATH-ANALYSIS", "GEOMETRY", "STATISTICS", "DATA STRUCTURES",
                "ALGORITHMS", "ECONOMY", "C-PROGRAMMING", "OOP", "PROGRAMMING HISTORY", "MATH HISTORY", "ADVANCED-METHODS",
                "WEB PROGRAMMING", "MOBILE PROGRAMMING", "CYBER-SECURITY", "FRONT-END DESIGN", "DATABASES"]
    for i in range(20):
        while True:
            id = randint(500, 600)
            if id not in data.keys():
                break
        discipline = elements[i]
        discipline = Discipline(id, discipline)
        data[id] = discipline
    return data


def random_grade(stud_data: dict, disc_data: dict) -> dict:
    grade_data: dict = {}
    stud_keys = list(stud_data.keys())
    disc_keys = list(disc_data.keys())
    for i in range(20):
        key: tuple = (stud_keys[i], disc_keys[i])
        grade_data[key] = [randint(0, 10) for _ in range(10)]
    return grade_data



class StudentMemoryRepo:
    def __init__(self):
        self._data = {}

    def add(self, student: Student):
        """
        Adds a student to the repository.
        :param student: the student that should be added
        :return:
        """
        if student.id in self._data:
            raise DuplicateIDError()
        elif student.name == "":
            raise InvalidNameError()
        self._data[int(student.id)] = student

    def remove(self, student_id: int):
        """
        Removes a student from the repository.
        :param student_id: id of the student that should be removed
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif int(student_id) not in self._data.keys():
            raise IDNotFoundError()
        student = self._data.pop(int(student_id))
        return student

    def find_id(self, stud_id: int) -> Student:
        """
        Finds the student with the given id in the repository.
        :param stud_id: the student's id
        :return: the student
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif stud_id not in self._data:
            raise IDNotFoundError()
        return self._data[stud_id]

    def find_name(self, stud_name: str) -> list:
        """
        Finds the student with the given name in the repository.
        :param stud_name: the student's name
        :return: the student
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif stud_name == "":
            raise InvalidNameError
        stud_name = stud_name.upper()
        lst = []
        ok = False
        for student in self._data.values():
            if stud_name in student.name:
                lst.append(student)
                ok = True
        if ok:
            return lst
        else:
            raise NameNotFoundError()

    def update_name(self, new_name: str, student_id: int):
        """
        Updates the student with the given name in the repository.
        :param new_name: the new name that should be updated
        :param student_id: the student's id'
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        if new_name == "":
            raise InvalidNameError()
        if student_id not in self._data.keys():
            raise IDNotFoundError()
        our_student = self.find_id(student_id)
        our_student.name = new_name.upper()

    def erase_all(self):
        """
        Deletes every element from the repository.
        :return:
        """
        keys = list(self._data.keys())
        for key in keys:
            self._data.pop(key)

    def __iter__(self):
        return RepositoryIterator(list(self._data.values()))

    def __len__(self):
        return len(self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data


class DisciplineMemoryRepo:
    def __init__(self):
        self._data = {}

    def add(self, discipline: Discipline):
        """
        Adds a discipline to the repository.
        :param discipline: the discipline that should be added
        :return:
        """
        if discipline.name == "":
            raise InvalidNameError()
        elif discipline.name in self._data:
            raise DuplicateNameError
        elif discipline.id in self._data:
            raise DuplicateIDError()
        self._data[discipline.id] = discipline

    def remove(self, discipline_id: int):
        """
        Removes a discipline from the repository.
        :param discipline_id: discipline's id
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif discipline_id not in self._data.keys():
            raise IDNotFoundError()
        discipline = self._data.pop(discipline_id)
        return discipline

    def find_id(self, discipline_id: int) -> Discipline:
        """
        Finds the discipline with the given id in the repository.
        :param discipline_id: discipline's id
        :return: the discipline
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif discipline_id not in list(self._data.keys()):
            raise IDNotFoundError()
        return self._data[discipline_id]

    def find_name(self, discipline_name: str):
        """
        Finds the discipline with the given name in the repository.
        :param discipline_name: the discipline's name
        :return: the discipline
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif discipline_name == "":
            raise InvalidNameError()
        lst = []
        ok = False
        discipline_name = discipline_name.upper()
        for discipline in self._data.values():
            if discipline_name in discipline.name:
                lst.append(discipline)
                ok = True
        if ok:
            return lst
        else:
            raise NameNotFoundError()

    def update_name(self, new_name: str, discipline_id: int):
        """
        Updates the discipline with the given name in the repository.
        :param new_name: the new name that should be updated
        :param discipline_id: discipline's id
        :return:
        """
        try:
            our_discipline = self.find_id(discipline_id)
        except EmptyRepositoryError:
            raise EmptyRepositoryError()
        except IDNotFoundError:
            raise IDNotFoundError()
        if new_name == "":
            raise InvalidNameError()
        our_discipline.name = new_name.upper()

    def erase_all(self):
        """
        Deletes every element from the repository.
        :return:
        """
        keys = list(self._data.keys())
        for key in keys:
            self._data.pop(key)

    def __iter__(self):
        return RepositoryIterator(list(self._data.values()))

    def __len__(self):
        return len(self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data


class GradeMemoryRepo:
    def __init__(self, student_memo_repo: StudentMemoryRepo, discipline_memo_repo: DisciplineMemoryRepo):
        self._student_memo_repo = student_memo_repo
        self._discipline_memo_repo = discipline_memo_repo
        self._data: dict = {}
        # key must be (student.id, discipline.id) !!!
        # _data = { (student.id, discipline.id) = [grade.values], etc... }

    def add(self, grade: Grade):
        """
        Adds a new grade to the repository.
        :param grade: the grade that should be added
        :return:
        """
        if grade.student_id not in self._student_memo_repo.data: # if there is no match between the keys,
        # I can't add a grade to a student/ discipline that doesn't exist.
            raise IDNotFoundError()
        elif grade.discipline_id not in self._discipline_memo_repo.data:
            raise IDNotFoundError()
        elif grade.grade_value < 0 or grade.grade_value > 10:
            raise InvalidGradeError()
        key = (grade.student_id, grade.discipline_id)
        if key in self._data:
            self._data[key].append(grade.grade_value)
        else:
            self._data[key] = [grade.grade_value]

    def remove_discipline(self, discipline_id: int):
        """
        Removes a discipline from the repository.
        :param discipline_id: the discipline's id
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError
        ok = False
        data_keys: list = list(self._data.keys())
        for i in range(len(data_keys)):
            if data_keys[i][1] == discipline_id:
                self._data.pop(data_keys[i])
                # self._discipline_memo_repo.remove(discipline_id)
                ok = True
        if not ok:
            raise IDNotFoundError()

    def remove_student(self, student_id: int):
        """
        Removes a student from the repository.
        :param student_id: student's id
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        ok = False
        data_keys: list = list(self._data.keys())
        for i in range(len(data_keys)):
            if data_keys[i][0] == student_id:
                self._data.pop(data_keys[i])
                # self._student_memo_repo.remove(student_id)
                ok = True
        if not ok:
            raise IDNotFoundError()
        # this may sometimes appear because the student exists in the student_repo, but not in the grades_repo also
        # (doesn't have any grade)

    def remove_grade(self, student_grade: Grade):
        """
        Removes a student's grade at a discipline from the repository.
        :param student_grade: the student's grade
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif student_grade.discipline_id not in self._discipline_memo_repo.data:
            raise IDNotFoundError()
        elif student_grade.student_id not in self._student_memo_repo.data:
            raise IDNotFoundError()
        ok = False
        key = (student_grade.student_id, student_grade.discipline_id)
        for keys in self._data.keys():
            if keys == key:
                ok = True
                for i in range(len(self._data[key])):
                    if self._data[key][i] == student_grade.grade_value:
                        self._data[key].pop(i)
                        break
        if not ok:
            raise GradeNotFoundError()

    def find_grades(self, stud_id: int, discipline_id: int) -> list:
        """
        Finds all the student's grades at that discipline and returns them.
        :param stud_id: the student's id
        :param discipline_id: the discipline's id
        :return: a list with the student's grades at that discipline
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        key = (stud_id, discipline_id)
        data_keys: list = list(self._data.keys())
        for i in range(len(data_keys)):
            if data_keys[i] == key:
                return self._data[key]
        raise IDNotFoundError()

    def update_grade(self, new_grade: int, actual_grade: Grade):
        """
        Updates a student's grades at a discipline with some new, given grades.
        :param new_grade: the new grade
        :param actual_grade: the old grade that should be updated
        :return:
        """
        if not self._data.values():
            raise EmptyRepositoryError()
        elif new_grade < 0 or new_grade > 10:
            raise InvalidGradeError()
        ok = False
        try:
            grades = self.find_grades(actual_grade.student_id, actual_grade.discipline_id)
            key = (actual_grade.student_id, actual_grade.discipline_id)
            for i in range(len(grades)):
                if grades[i] == actual_grade.grade_value:
                    grades[i] = new_grade
                    ok = True
                    break
            self._data[key] = grades
        except IDNotFoundError:
            raise IDNotFoundError()
        except not ok:
            raise GradeNotFoundError()

    def erase_all(self):
        """
        Deletes every element from the repository.
        :return:
        """
        keys = list(self._data.keys())
        for key in keys:
            self._data.pop(key)

    def __iter__(self):
        return RepositoryIterator(list(self._data.values()))

    def __len__(self):
        return len(self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data

