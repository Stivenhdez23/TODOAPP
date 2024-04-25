from datetime import datetime, timedelta
from services import _get_complexity
from unittest.mock import patch
from services import _get_teacher
from services import _extract_subject
from services import _get_classroom
from unittest.mock import Mock
from services import get_task_by_id, DatabaseAdapter
from services import create_task, DatabaseAdapter, _get_deadline, _get_complexity, _get_teacher, _get_classroom
from typing import Dict
from models import Task
import unittest

########### PUNTOS OPCIONALES - PRUEBAS DE INTEGRACION ############
#1
class TestGetTaskByIdIntegration(unittest.TestCase):
    def test_get_task_by_id_integration(self):
        # Configurar una base de datos simulada con una tarea de ejemplo
        db_mock = Mock(spec=DatabaseAdapter)
        example_task_id = 1
        example_task_data = {'id': example_task_id, 'title': 'Example Task', 'description': 'This is an example task'}
        db_mock.get_task_by_id.return_value = example_task_data

        # Llamar a la función que quieres probar
        result = get_task_by_id(example_task_id, db_mock)

        # Verificar que se haya llamado a get_task_by_id con el ID correcto
        db_mock.get_task_by_id.assert_called_once_with(example_task_id)

        # Verificar que el resultado es el esperado
        self.assertEqual(result, example_task_data)

if __name__ == '__main__':
    unittest.main()

#2
class TestCreateTaskIntegration(unittest.TestCase):
    def test_create_task_integration(self):
        # Configurar una base de datos simulada
        db_mock = Mock(spec=DatabaseAdapter)

        # Definir los datos de la tarea
        task_data = {
            'title': 'Example Task',
            'description': 'This is an example task'
        }

        # Obtener la fecha límite
        deadline = (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")

        # Obtener la complejidad
        complexity = "Fácil"

        # Obtener el profesor
        teacher = "Profesor A"

        # Obtener el aula
        classroom = "Aula 101"

        # Crear un objeto Task
        task_model = Task(**task_data, deadline=deadline, complexity=complexity, teacher=teacher, classroom=classroom)

        # Configurar la base de datos simulada para devolver el ID de la tarea creada
        db_mock.create_task.return_value = 1

        # Llamar a la función que quieres probar
        result = create_task(task_data, db_mock)

        # Verificar que se haya llamado a create_task con el objeto Task correcto
        db_mock.create_task.assert_called_once_with(task_model)

        # Verificar que el resultado es el esperado (el ID de la tarea creada)
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()

########### SEGUNDO CORTE - PRUEBAS UNITARIAS ######################
#1
def _get_deadline() -> str:
    return (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")

class TestGetDeadline(unittest.TestCase):
    def test_get_deadline(self):
        # Obtiene la fecha actual
        current_time = datetime.utcnow()

        # Calcula la fecha esperada agregando 8 días a la fecha actual
        expected_date = (current_time + timedelta(days=8)).strftime("%Y-%m-%d")

        # Obtiene la fecha real usando la función _get_deadline()
        actual_date = _get_deadline()

        # Comprueba si la fecha obtenida es igual a la esperada
        self.assertEqual(actual_date, expected_date)

if __name__ == '__main__':
    unittest.main()

#2
class TestGetComplexity(unittest.TestCase):
    def test_easy_complexity(self):
        description = "Una descripción corta"
        expected_result = "Fácil"
        actual_result = _get_complexity(description)
        self.assertEqual(actual_result, expected_result)

    def test_difficult_complexity(self):
        description = "Una descripción un poco más larga pero aún manejable"
        expected_result = "Difícil"
        actual_result = _get_complexity(description)
        self.assertEqual(actual_result, expected_result)

    def test_very_difficult_complexity(self):
        description = "Una descripción extremadamente larga que hará que la tarea sea muy difícil de realizar"
        expected_result = "Muy Difícil"
        actual_result = _get_complexity(description)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()

#3
class TestGetTeacher(unittest.TestCase):
    @patch('random.choice', return_value='Profesor G')
    def test_easy_complexity(self, mock_random_choice):
        description = "Una descripción corta"
        complexity = "Fácil"
        expected_result = "Profesor A"
        actual_result = _get_teacher(complexity, description)
        self.assertEqual(actual_result, expected_result)

    @patch('random.choice', return_value='Profesor E')
    def test_difficult_complexity(self, mock_random_choice):
        description = "Una descripción un poco más larga pero aún manejable"
        complexity = "Difícil"
        expected_result = "Profesor B"
        actual_result = _get_teacher(complexity, description)
        self.assertEqual(actual_result, expected_result)

    @patch('random.choice', return_value='Profesor G')
    def test_very_difficult_complexity_with_subject(self, mock_random_choice):
        description = "Una descripción extremadamente larga que hará que la tarea sea muy difícil de realizar. Programación Avanzada."
        complexity = "Muy Difícil"
        expected_result = "Profesor G"
        actual_result = _get_teacher(complexity, description)
        self.assertEqual(actual_result, expected_result)

    @patch('random.choice', return_value='Profesor por determinar')
    def test_very_difficult_complexity_without_subject(self, mock_random_choice):
        description = "Una descripción extremadamente larga que hará que la tarea sea muy difícil de realizar. Sin asignatura."
        complexity = "Muy Difícil"
        expected_result = "Profesor por determinar"
        actual_result = _get_teacher(complexity, description)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()

#4
class TestExtractSubject(unittest.TestCase):
    def test_extract_subject(self):
        description = "Una descripción que incluye la asignatura de Matemáticas"
        expected_result = "Matemáticas"
        actual_result = _extract_subject(description)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()

#5
class TestGetClassroom(unittest.TestCase):
    def test_easy_complexity(self):
        complexity = "Fácil"
        current_hour = 10  # Hora de la mañana
        expected_result = "Aula 101"
        actual_result = _get_classroom(complexity, current_hour)
        self.assertEqual(actual_result, expected_result)

    def test_difficult_complexity(self):
        complexity = "Difícil"
        current_hour = 14  # Hora de la tarde
        expected_result = "Aula 201"
        actual_result = _get_classroom(complexity, current_hour)
        self.assertEqual(actual_result, expected_result)

    def test_very_difficult_complexity_morning(self):
        complexity = "Muy Difícil"
        current_hour = 10  # Hora de la mañana
        expected_result = "Aula 301"
        actual_result = _get_classroom(complexity, current_hour)
        self.assertEqual(actual_result, expected_result)

    def test_very_difficult_complexity_afternoon(self):
        complexity = "Muy Difícil"
        current_hour = 14  # Hora de la tarde
        expected_result = "Aula 302"
        actual_result = _get_classroom(complexity, current_hour)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()