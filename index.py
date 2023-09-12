from flask import Flask, render_template, request, make_response
from celery import Celery
import compobador_ofertas
from config import Config
import time

app = Flask(__name__)

celery = Celery('index', backend='rpc://', broker='pyamqp://')


@celery.task
def add(x: int, y: int) -> int:
    time.sleep(3)
    return x * y


@app.route('/', methods=['GET', 'POST'])
def home():
    task1 = add.delay(7, 89)
    sum1 = task1.wait(timeout=30, interval=1)
    print(sum1)
    user_input = request.form
    print(user_input)
    if request.method == 'POST':
        email = request.form['emailInput']
        url = request.form['urlInput']
        compobador_ofertas.check_sale(email, url)
        return render_template('about.html')
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
