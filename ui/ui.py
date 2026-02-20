from src.repository.repo_memory import *
from src.repository.repo_text import *
from src.repository.repo_binary import *
from src.services.student_service import *
from src.services.discipline_service import *
from src.services.grade_service import *
from texttable import Texttable
from src.services.student_service import *


class Ui():
    def __init__(self, student_service: StudentService, discipline_service: DisciplineService, grade_service: GradeService, undo_service: UndoService):
        self.__student_service = student_service
        self.__discipline_service = discipline_service
        self.__grade_service = grade_service
        self.__undo_service = undo_service

    def menu(self):
        print("0. Exit")
        print("1.1 Add a new student")
        print("1.2 Add a new discipline")
        print("1.3 Add a new grade\n")
        print("2.1 Remove a student")
        print("2.2 Remove a discipline")
        print("2.3 Remove a grade\n")
        print("3.1 Update a student")
        print("3.2 Update a discipline")
        print("3.3 Update a grade\n")
        print("4.1 List all students")
        print("4.2 List all disciplines")
        print("4.3 List all grades of a student at a discipline\n")
        print("5.1.1 Search a student by ID")
        print("5.1.2 Search a student by name")
        print("5.2.1 Search a discipline by ID")
        print("5.2.2 Search a discipline by name\n")
        print("6.1 Undo")
        print("6.2 Redo\n")

    def option(self):
        while True:
            try:
                option = input(">").strip().split(".")
                if len(option) == 2:
                    option.append("0") # if option has only two numbers, I add a 0 to the end to avoid some errors from below
                elif len(option) == 1 and option[0] == "0":
                    option = ["0", "0", "0"]
                    break
                elif len(option)==3:
                    pass
                else:
                    raise ValueError

                if not option[0].isdigit() or not option[1].isdigit() or not option[2].isdigit():
                    raise ValueError
                elif int(option[0]) > 6:
                    raise ValueError
                elif (int(option[0]) == 5) and (int(option[1])>2 or int(option[1])<1 or int(option[2])>2 or int(option[2])<1):
                    raise ValueError
                elif (int(option[1]) > 3) or (int(option[1]) < 1):
                    raise ValueError
                elif (int(option[0]) < 0) or (int(option[1]) < 0) or (int(option[2]) < 0):
                    raise ValueError
                break
            except ValueError:
                print("\nInvalid option. Try again\n")
        return option

    def ui_load(self):
        try:
            self.__student_service.load()
            self.__discipline_service.load()
            self.__grade_service.load()
        except AttributeError:
            pass

    def start(self):
        while True:
            self.menu()
            option = self.option()

            if option[0] == "0":
                break

            elif option[0] == "1":

                if option[1] == "1": #"Add a new student"
                    while True:
                        try:
                            student_id = int(input("Student ID: "))
                            student_name = input("Student Name: ")
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    student = Student(student_id, student_name)
                    try:
                        self.__student_service.add(student)
                    except DuplicateIDError:
                        print("\nStudent ID already exists\n")

                elif option[1] == "2": #"Add a new discipline"
                    while True:
                        try:
                            discipline_id = int(input("Discipline ID: "))
                            discipline_name = input("Discipline Name: ")
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    discipline = Discipline(discipline_id, discipline_name)
                    try:
                        self.__discipline_service.add(discipline)
                    except DuplicateNameError:
                        print("\nDiscipline Name already exists\n")
                    except InvalidNameError:
                        print("\nInvalid option. Try again\n")
                    except DuplicateIDError:
                        print("\nDiscipline ID already exists\n")

                elif option[1] == "3": #"Add a new grade"
                    while True:
                        try:
                            student_id = int(input("Student ID: "))
                            discipline_id = int(input("Discipline ID: "))
                            grade_value = int(input("Grade value: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    grade = Grade(student_id, discipline_id, grade_value)
                    try:
                        self.__grade_service.add(grade)
                    except IDNotFoundError:
                        print("\nThe student's/ discipline's ID does not exist\n")
                    except InvalidGradeError:
                        print("\nInvalid grade. Please try again\n")

            elif option[0] == "2":

                if option[1] == "1": # Remove a student
                    while True:
                        try:
                            stud_id = int(input("Student ID: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    try:
                        self.__grade_service.remove_student(stud_id)
                        self.__student_service.remove(stud_id) # TODO poate trebuie sa elimin studentul in try-uri diferite...
                    except EmptyRepositoryError:
                        print("\nThe repository is empty and cannot do this operation\n")
                    except IDNotFoundError:
                        print("\nThe student's ID does not exist\n")

                elif option[1] == "2": # Remove a discipline
                    while True:
                        try:
                            discipline_id = int(input("Discipline ID: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    try:
                        self.__grade_service.remove_discipline(discipline_id)
                        self.__discipline_service.remove(discipline_id)
                    except EmptyRepositoryError:
                        print("\nThe repository is empty and cannot do this operation\n")
                    except IDNotFoundError:
                        print("\nThe discipline's ID does not exist\n")

                elif option[1] == "3": # Remove a grade
                    while True:
                        try:
                            stud_id = int(input("Student ID: "))
                            discipline_id = int(input("Discipline ID: "))
                            grade_value = int(input("Grade value: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    grade = Grade(stud_id, discipline_id, grade_value)
                    try:
                        self.__grade_service.remove_grade(grade)
                    except EmptyRepositoryError:
                        print("\nThe repository is empty and cannot do this operation\n")
                    except IDNotFoundError:
                        print("\nThe student's/ discipline's ID does not exist\n")
                    except GradeNotFoundError:
                        print("\nThe grade's value does not exist\n")

            elif option[0] == "3":

                if option[1] == "1": # Update a student
                    while True:
                        try:
                            new_name = input("New Name: ")
                            stud_id = int(input("Student ID: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    try:
                        self.__student_service.update_name(new_name, stud_id)
                    except EmptyRepositoryError:
                        print("\nThe repository is empty and cannot do this operation\n")
                    except IDNotFoundError:
                        print("\nThe student's ID does not exist\n")

                elif option[1] == "2": # Update a discipline
                    while True:
                        try:
                            new_name = input("New Name: ")
                            discipline_id = int(input("Discipline ID: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    try:
                        self.__discipline_service.update_name(new_name, discipline_id)
                    except EmptyRepositoryError:
                        print("\nThe repository is empty and cannot do this operation\n")
                    except IDNotFoundError:
                        print("\nThe discipline's ID does not exist\n")
                    except InvalidNameError:
                        print("\nInvalid name. Please try again\n")

                elif option[1] == "3": # Update a grade
                    while True:
                        try:
                            old_value = int(input("Old Grade: "))
                            student_id = int(input("Student ID: "))
                            discipline_id = int(input("Discipline ID: "))
                            new_value = int(input("New Grade: "))
                            break
                        except ValueError:
                            print("\nInvalid option. Try again\n")
                    old_grade = Grade(student_id, discipline_id, old_value)
                    try:
                        self.__grade_service.update_grade(new_value, old_grade)
                    except EmptyRepositoryError:
                        print("\nThe repository is empty and cannot do this operation\n")
                    except InvalidGradeError:
                        print("\nInvalid grade. Please try again\n")
                    except IDNotFoundError:
                        print("\nThe student's/ discipline's ID does not exist\n")
                    except GradeNotFoundError:
                        print("\nThe grade's value does not exist\n")

            elif option[0] == "4":
                if option[1] == "1": # List all students
                    table = Texttable()
                    table.add_row(["Student ID", "Student Name"])
                    lst = self.__student_service.get_all()
                    for student in lst.values():
                        table.add_row([str(student.id), student.name])
                    print(table.draw())

                elif option[1] == "2": # List all disciplines
                    table = Texttable()
                    table.add_row(["Discipline ID", "Discipline Name"])
                    lst = self.__discipline_service.get_all()
                    for discipline in lst.values():
                        table.add_row([str(discipline.id), discipline.name])
                    print(table.draw())

                elif option[1] == "3": # List all grades
                    table = Texttable()
                    table.add_row(["Student ID", "Discipline ID", "Grades"])
                    data_keys = list(self.__grade_service.get_all().keys())
                    data_values = list(self.__grade_service.get_all().values())
                    for i in range(len(data_keys)):
                        table.add_row([str(data_keys[i][0]), str(data_keys[i][1]), data_values[i]])
                    print(table.draw())

            elif option[0] == "5":
                if option[1] == "1":
                    if option[2] == "1": # Search a student by ID
                        while True:
                            try:
                                stud_id = int(input("Student ID: "))
                                break
                            except ValueError:
                                print("\nInvalid option. Try again\n")
                        try:
                            student = self.__student_service.find_id(stud_id)
                            print(student.__str__())
                        except EmptyRepositoryError:
                            print("\nThe repository is empty and cannot do this operation\n")
                        except IDNotFoundError:
                            print("\nThe ID '" + str(stud_id) + "' does not exist\n")

                    elif option[2] == "2": # Search a student by name
                        while True:
                            try:
                                name = input("Student's Name: ")
                                break
                            except ValueError:
                                print("\nInvalid option. Try again\n")
                        try:
                            lst = self.__student_service.find_name(name)
                            for student in lst:
                                print(student.__str__())
                        except EmptyRepositoryError:
                            print("\nThe repository is empty and cannot do this operation\n")
                        except InvalidNameError:
                            print("\nThe name introduced is not a valid one\n")
                        except NameNotFoundError:
                            print("\nThe name '" + name + "' does not exist\n")

                elif option[1] == "2":
                    if option[2] == "1": # Search a discipline by ID
                        while True:
                            try:
                                discipline_id = int(input("Discipline ID: "))
                                break
                            except ValueError:
                                print("\nInvalid option. Try again\n")
                        try:
                            discipline = self.__discipline_service.find_id(discipline_id)
                            print(discipline.__str__())
                        except EmptyRepositoryError:
                            print("\nThe repository is empty and cannot do this operation\n")
                        except IDNotFoundError:
                            print("\nThe ID '" + str(discipline_id) + "' does not exist\n")

                    elif option[2] == "2": # Search a discipline by name
                        while True:
                            try:
                                name = input("Discipline's Name: ")
                                break
                            except ValueError:
                                print("\nInvalid option. Try again\n")
                        try:
                            lst = self.__discipline_service.find_name(name)
                            for discipline in lst:
                                print(discipline.__str__())
                        except EmptyRepositoryError:
                            print("\nThe repository is empty and cannot do this operation\n")
                        except InvalidNameError:
                            print("\nThe name introduced is not a valid one\n")
                        except NameNotFoundError:
                            print("\nThe name '" + name + "' does not exist\n")

            elif option[0] == "6":
                if option[1] == "1":
                    try:
                        self.__undo_service.undo()
                    except UndoRedoError:
                        print("\nNo more undos!\n")

                elif option[1] == "2":
                    try:
                        self.__undo_service.redo()
                    except UndoRedoError:
                        print("\nNo more redos!\n")

