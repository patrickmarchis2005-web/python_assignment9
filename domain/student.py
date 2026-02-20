class Student(object):
    def __init__(self, student_id: int, student_name: str):
        self.__student_id = student_id
        self.__student_name = student_name.upper()

    @property
    def id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__student_name

    @name.setter
    def name(self, name: str):
        self.__student_name = name.upper()

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id) + "," + self.name + "\n"



# if __name__ == "__main__":
#     c1 = Student(1000, "Popescu Ana")
#     c2 = Student(1001, "Popescu Ana")
#     print(c1.__eq__(c2))
#     print(c1 == c2)
#     print(c1.__str__())


