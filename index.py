from flask import Flask, render_template, request, make_response
from celeryapp import celery
import compobador_ofertas
from config import Config
import time

app = Flask(__name__)


@celery.task
def add(x: int, y: int) -> int:
    time.sleep(10)
    return x * y


@app.route('/', methods=['GET', 'POST'])
def home():
    task1 = add.delay(7, 3)
    sum1 = task1.wait(timeout=30, interval=1)

    user_input = request.form
    print(user_input)
    if request.method == 'POST':
        email = request.form['emailInput']
        url = request.form['urlInput']
        compobador_ofertas.check_sale.delay(email, url)
        return render_template('about.html')
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
