import re
import sys
import urllib.request

import envio_email
from time import sleep
from celeryapp import celery
from requests_html import HTMLSession
from urllib.parse import urlparse
from index import flash
session = HTMLSession()


def buscar_tienda(url):
    # Los nombres y los diferentes atributos que tienes la paginas para etiquetar que un producto esta rebajado
    tiendas = [
        ("asos", 'discountPercentage":0'),
        ("boohooman", 'price-sales-red'),
        ("bstn", '<span class="percentage-savings">-')
    ]

    nombres = [nombre for nombre, _ in tiendas]
    codigos = [codigo for _, codigo in tiendas]

    # Se junta los nombres de las tiendas separados por barra
    tiendas_regexp = "|".join(nombres)
    # Se comprueba que algun nombre coincida con la url
    match = re.search(tiendas_regexp, url)

    if match:
        # Se comprueba que indice tiene la tienda que coincide
        indice = nombres.index(match.group(0))
        return codigos[indice], nombres[indice]


def comprobacion_de_datos(email_usu, urls_usu):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_valido = True
    if not re.fullmatch(regex, email_usu):
        email_valido = False
        flash(
            ' ⚠️ has introducido mal el email:{} '.format(email_usu))

    urls = urls_usu.split(',')
    urls_validas = True  # Suponemos que todas las URLs son válidas hasta que se demuestre lo contrario

    for url in urls:
        try:
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                flash(
                    ' ⚠️ has metido mal esta url: {}'.format(url))
                urls_validas = False  # Si encontramos una URL no válida, actualizamos la variable a False
                break  # No es necesario seguir comprobando las otras URLs si una no es válida
        except ValueError:
            urls_validas = False
            flash(' ⚠️ has introducido mal esta url: {}'.format(url))
            break

    return email_valido and urls_validas


# operacion con celery task lo que signfica que se puede ejecutar en segundo plano
@celery.task
def check_sale(email_usu, urls_usu):
    rebajados = False
    urls = urls_usu.split(',')
    # Lista para llevar registro de URLs rebajados
    rebajados_lista = []

    while not rebajados:

        rebajados = True

        for url in urls:

            # Se recoge el contenido de la pagina
            content_page = session.get(url)

            key_to_find, tienda = buscar_tienda(url)

            # Se busca si el atributo de descuento de la pagina esta presente en el contenido
            on_sale = content_page.text.find(key_to_find)

            if key_to_find == "price-sales-red" or key_to_find == '<span class="percentage-savings">-':
                if on_sale == -1:
                    print(f"Todavia no esta rebajado: {url}")
                    rebajados = False
                else:
                    # Verificar que no se haya enviado antes
                    if url not in rebajados_lista:
                        print(f"Esta rebajado: {url}")
                        envio_email.enviar_email(email_usu, tienda, url)
                        # Marcar como procesado
                        rebajados_lista.append(url)

            else:
                if on_sale == -1:
                    # Verificar que no se haya enviado antes
                    if url not in rebajados_lista:
                        print(f"Esta rebajado: {url}")
                        envio_email.enviar_email(email_usu, tienda, url)
                        # Marcar como procesado
                        rebajados_lista.append(url)
                else:
                    print(f"Todavia no esta rebajado: {url}")
                    rebajados = False

        if not rebajados:
            # Si alguno no está rebajado, espera 10 minutos y se vuelve a ejecutar
            sleep(600)
