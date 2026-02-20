from enum import Enum


class RepositoryType(Enum):
    MEMORY = 0
    TEXT_FILE = 1
    BINARY_FILE = 2


class Settings:
    __instance = None

    @staticmethod
    def get_instance():
        if Settings.__instance is not None:
            return Settings.__instance
        fin = open("settings.properties", "rt")
        file_lines = fin.readlines()
        fin.close()

        settings_dict = {}
        for line in file_lines:
            if line.strip().startswith("#"):
                continue
            tokens = line.strip().split("=")
            settings_dict[tokens[0].strip()] = tokens[1].strip()

        repo_type = settings_dict["repository"]
        students_file = settings_dict["student_file"]
        disciplines_file = settings_dict["discipline_file"]
        grades_file = settings_dict["grade_file"]

        repository_type = RepositoryType.MEMORY
        if repo_type == "textfile":
            repository_type = RepositoryType.TEXT_FILE
        elif repo_type == "binaryfile":
            repository_type = RepositoryType.BINARY_FILE

        Settings.__instance = Settings(repository_type, students_file, disciplines_file, grades_file)
        return Settings.__instance

    def __init__(self, repo_type: RepositoryType, students_file: str, disciplines_file: str, grades_file: str):
        self.__repo_type = repo_type
        self.__students_file = students_file
        self.__disciplines_file = disciplines_file
        self.__grades_file = grades_file

    @property
    def repository_type(self):
        return self.__repo_type

    @property
    def students_file(self):
        return self.__students_file

    @property
    def disciplines_file(self):
        return self.__disciplines_file

    @property
    def grades_file(self):
        return self.__grades_file
