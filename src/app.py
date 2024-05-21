from flask import Flask, request, jsonify, render_template
import logging
from sympy import sympify, SympifyError, N

app = Flask(__name__)

logging.basicConfig(filename='logs/operations.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form.get('expression')
    
    # Проверка на наличие букв в выражении
    if any(char.isalpha() for char in expression):
        app.logger.error(f'Invalid input: {expression}')
        return jsonify(status="error", result="Invalid input"), 400
    
    try:
        result = sympify(expression) #Вычисление
        result = N(result)  # Преобразование в число с плавающей запятой
        result = str(result).rstrip("0").rstrip(".") #Отсечение лишних нулей
        app.logger.info(f'User input: {expression}, Result: {result}')
        return jsonify(status="success", result=str(result))
    except (SympifyError, ValueError) as e:
        # Логирование ошибки и возврат сообщения пользователю
        app.logger.error(f'Error in user input: {expression}, Error: {str(e)}')
        return jsonify(status="error", result="Incorrect expression"), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1')
