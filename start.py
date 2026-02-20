from src.repository.repo_memory import StudentMemoryRepo, DisciplineMemoryRepo, GradeMemoryRepo, random_students, \
    random_discipline, random_grade
from src.repository.repo_text import StudentFileRepo, DisciplineFileRepo, GradeFileRepo
from src.repository.repo_binary import StudentBinRepo, DisciplineBinRepo, GradeBinRepo
from src.services.student_service import StudentService
from src.services.discipline_service import DisciplineService
from src.services.grade_service import GradeService
from src.settings import Settings, RepositoryType
from src.ui.ui import Ui


students_repo = None
disciplines_repo = None
grades_repo = None


if Settings.get_instance().repository_type == RepositoryType.MEMORY:
    students_repo = StudentMemoryRepo()
    disciplines_repo = DisciplineMemoryRepo()
    grades_repo = GradeMemoryRepo(students_repo, disciplines_repo)

elif Settings.get_instance().repository_type == RepositoryType.TEXT_FILE:
    students_repo = StudentFileRepo(Settings.get_instance().students_file)
    disciplines_repo = DisciplineFileRepo(Settings.get_instance().disciplines_file)
    grades_repo = GradeFileRepo(students_repo, disciplines_repo, Settings.get_instance().grades_file)

elif Settings.get_instance().repository_type == RepositoryType.BINARY_FILE:
    students_repo = StudentBinRepo(Settings.get_instance().students_file)
    disciplines_repo = DisciplineBinRepo(Settings.get_instance().disciplines_file)
    grades_repo = GradeBinRepo(students_repo, disciplines_repo, Settings.get_instance().grades_file)

if len(students_repo.data) == 0:
    students_repo.data = random_students()
    students_repo.save()
if len(disciplines_repo.data) == 0:
    disciplines_repo.data = random_discipline()
    disciplines_repo.save()
if len(grades_repo.data) == 0:
    grades_repo.data = random_grade(students_repo.data, disciplines_repo.data)
    grades_repo.save()

students_service = StudentService(students_repo)
disciplines_service = DisciplineService(disciplines_repo)
grades_service = GradeService(grades_repo)

ui = Ui(students_service, disciplines_service, grades_service)
ui.start()
