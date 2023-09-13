from email.message import EmailMessage
import ssl
import smtplib
import os


def enviar_email(destinatario, tienda, enlace):
    remitente = "victormcclase@gmail.com"
    contrasena = os.environ['EMAIL_PASSWORD']

    asunto = "Aprovecha ahora el producto de {} esta en oferta".format(tienda)
    mensaje = """Estas de suerte el producto de {} esta en descuento
    aquí tienes el enlace: {}
    """.format(tienda, enlace)

    em = EmailMessage()
    em['From'] = remitente
    em['To'] = destinatario
    em['Subject'] = asunto
    em.set_content(mensaje)

    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(remitente, contrasena)
        smtp.sendmail(remitente, destinatario, em.as_string())
