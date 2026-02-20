class Grade:
    def __init__(self, student_id, discipline_id, grade_value):
        self.__discipline_id = discipline_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def discipline_id(self):
        return self.__discipline_id

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grade_value(self):
        return self.__grade_value

    @grade_value.setter
    def grade_value(self, value):
        self.__grade_value = value

    def __str__(self):
        return str(self.discipline_id) + "," + str(self.student_id) + "," + str(self.grade_value) + "\n"

