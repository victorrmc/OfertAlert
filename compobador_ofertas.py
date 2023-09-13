import re
import sys
import envio_email
from time import sleep
from celeryapp import celery
from requests_html import HTMLSession

session = HTMLSession()


def buscar_tienda(url):
    tiendas = [
        ("asos", 'discountPercentage":0'),
        ("boohooman", 'price-sales-red'),
        ("bstn", '<span class="percentage-savings">-')
    ]

    nombres = [nombre for nombre, _ in tiendas]
    codigos = [codigo for _, codigo in tiendas]

    tiendas_regexp = "|".join(nombres)
    match = re.search(tiendas_regexp, url)

    if match:
        indice = nombres.index(match.group(0))
        return codigos[indice], nombres[indice]


@celery.task
def check_sale(email_usu, urls_usu):
    bool = True
    urls = urls_usu.split(',')

    while bool:
        for url in urls:
            content_page = session.get(url)
            key_to_find, tienda = buscar_tienda(url)

            on_sale = content_page.text.find(key_to_find)

            if key_to_find == "price-sales-red" or key_to_find == '<span class="percentage-savings">-':
                if on_sale == -1:
                    print(f"Todavia no esta rebajado: {url}")
                else:
                    print(f"Esta rebajado: {url}")
                    envio_email.enviar_email(email_usu, tienda, url)
                    bool = False
            else:
                if on_sale == -1:
                    print(f"Esta rebajado: {url}")
                    envio_email.enviar_email(email_usu, tienda, url)
                    bool = False
                else:
                    print(f"Todavia no esta rebajado: {url}")

        if bool:
            sleep(600)

    print("Se enviaron los emails correctamente")
