from flask import Flask, render_template, request, make_response
from celeryapp import celery
import compobador_ofertas

import time

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['emailInput']
        url = request.form['urlInput']

        compobador_ofertas.check_sale.delay(email, url)
        return render_template('index.html')
        #return render_template('about.html')
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
