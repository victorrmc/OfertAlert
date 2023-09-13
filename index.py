from flask import Flask, render_template, request, make_response, flash
from celeryapp import celery
import compobador_ofertas

import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['emailInput']
        url = request.form['urlInput']
        resultado = compobador_ofertas.comprobacion_de_datos(email, url)
        if resultado:
            compobador_ofertas.check_sale.delay(email, url)
            flash(
                '✔️ Tus productos se han regitrado correctamente cuando esten en oferta se te avisara a este correo {}'.format(
                    email))

        return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
