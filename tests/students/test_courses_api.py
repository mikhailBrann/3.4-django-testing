import pytest
from random import sample as randomSampleList
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course

base_path = '/api/v1'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        new_student = baker.make(Student, *args, **kwargs)
        return new_student

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


# проверка получения 1го курса
@pytest.mark.django_db
def test_first_course(client, student_factory, course_factory):
    # Arrange
    students = student_factory(_quantity=25)
    course = course_factory(name='Python', students=students)

    #Act
    response = client.get(f"{base_path}/courses/{course.id}/")
    data = response.json()

    #Assert
    assert response.status_code == 200
    assert data['id'] == course.id
    assert data['name'] == course.name
    assert len(data['students']) == len(course.students.all())


# проверка получения списка курсов
@pytest.mark.django_db
def test_list_courses(client, student_factory, course_factory):
    #Arrange
    students = student_factory(_quantity=15)
    courses = course_factory(_quantity=3, students=randomSampleList(students, 3))

    #Act
    response = client.get(base_path + '/courses/')
    data = response.json()

    #Assert
    assert response.status_code == 200
    assert len(data) == Course.objects.count()


# проверка курсов по id
@pytest.mark.django_db
def test_course_id(client, student_factory, course_factory):
    # Arrange
    students = student_factory(_quantity=12)
    course = course_factory(students=randomSampleList(students, 3))

    # Act
    response = client.get(f"{base_path}/courses/?id={course.id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data[0]['id'] == course.id


# проверка курсов по name
@pytest.mark.django_db
def test_course_name(client, student_factory, course_factory):
    # Arrange
    students = student_factory(_quantity=12)
    course = course_factory(students=randomSampleList(students, 3))

    # Act
    response = client.get(f"{base_path}/courses/?name={course.name}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data[0]['name'] == course.name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    new_student = Student(name="Alex")
    new_student.save()

    # Act
    response = client.post(base_path + '/courses/', data={'name': 'python', 'students': [new_student.id]})

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == 1


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, student_factory, course_factory):
    # Arrange
    students = student_factory(_quantity=10)
    course = course_factory(name='Php', students=students)

    # Act
    new_course_name = 'Php + Laravel'
    response = client.patch(f"{base_path}/courses/{course.id}/", data={"name": new_course_name})

    #Assert
    assert response.status_code == 200


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, student_factory, course_factory):
    # Arrange
    students = student_factory(_quantity=10)
    course = course_factory(name='Php', students=students)

    # Act
    response = client.delete(f"{base_path}/courses/{course.id}/")

    # Assert
    assert response.status_code == 204



