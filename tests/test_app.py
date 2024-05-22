import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# проверка загрузки главной страницы
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>Calculator</title>' in response.data  

# проверка операции сложения
def test_calculate_addition(client):
    response = client.post('/calculate', data={'expression': '6 + 7'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['result'] == '13'

# проверка операции вычитания
def test_calculate_subtraction(client):
    response = client.post('/calculate', data={'expression': '5 - 3'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['result'] == '2'

# проверка результата равного нулю при вычитании
def test_calculate_subtraction_zero(client):
    response = client.post('/calculate', data={'expression': '5 - 5'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['result'] == '0'

# проверка операции умножения
def test_calculate_multiplication(client):
    response = client.post('/calculate', data={'expression': '3 * 4'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['result'] == '12'

# проверка операции умножения на ноль
def test_calculate_multiplication_zero(client):
    response = client.post('/calculate', data={'expression': '3 * 0'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['result'] == '0'

# проверка операции деления
def test_calculate_division(client):
    response = client.post('/calculate', data={'expression': '10 / 2'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['result'] == '5'

# проверка деления на ноль
def test_calculate_division_by_zero(client):
    response = client.post('/calculate', data={'expression': '2 / 0'})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['result'] == 'Incorrect expression'

# проверка ввода некорректных данных
def test_calculate_invalid_input(client):
    response = client.post('/calculate', data={'expression': '2 + a'})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['result'] == 'Invalid input'
