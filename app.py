from flask import Flask, request, jsonify, render_template
import logging
from sympy import sympify, SympifyError

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(filename='calculator.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form.get('expression')
    try:
        # Парсим и вычисляем выражение
        result = sympify(expression)
        app.logger.info(f'User input: {expression}, Result: {result}')
        return jsonify(status="success", result=str(result))
    except (SympifyError, ValueError) as e:
        app.logger.error(f'Error in user input: {expression}, Error: {str(e)}')
        return jsonify(status="error", result=str(e))

if __name__ == '__main__':
    app.run(debug=True)