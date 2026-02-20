class Discipline(object):
    def __init__(self, discipline_id: int, name: str):
        self.__discipline_id = discipline_id
        self.__discipline_name = name.upper()

    @property
    def id(self):
        return self.__discipline_id

    @property
    def name(self):
        return self.__discipline_name

    @name.setter
    def name(self, name: str):
        self.__discipline_name = name.upper()

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id) + "," + self.__discipline_name + "\n"


# if __name__ == '__main__':
#     math = Discipline(1, 'Math')
#     print(math)
#     print(math.discipline_id)
#     print(math.name)
#     print(math.__str__())
#     asc = Discipline(2, 'ASC')
#     print(asc)
#     print(math.__eq__(asc))
