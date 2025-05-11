import smtplib
import os
import mimetypes
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email import encoders


def send_email(sender_email, sender_password, recipient_email, subject, message, attachments=None,
               smtp_server="smtp.gmail.com", smtp_port=587):


    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Добавляем текст письма
    msg.attach(MIMEText(message, 'plain'))

    # Обрабатываем вложения
    if attachments:
        for file_path in attachments:
            if os.path.isfile(file_path):
                # Определяем тип файла
                ctype, encoding = mimetypes.guess_type(file_path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)

                # Читаем файл и добавляем его к письму
                with open(file_path, 'rb' if maintype != 'text' else 'r') as fp:
                    if maintype == 'text':
                        attachment = MIMEText(fp.read(), _subtype=subtype)
                    elif maintype == 'image':
                        attachment = MIMEImage(fp.read(), _subtype=subtype)
                    elif maintype == 'audio':
                        attachment = MIMEAudio(fp.read(), _subtype=subtype)
                    else:
                        attachment = MIMEBase(maintype, subtype)
                        attachment.set_payload(fp.read())
                        encoders.encode_base64(attachment)

                # Устанавливаем заголовки для вложения
                filename = os.path.basename(file_path)
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment)

    # Устанавливаем соединение с сервером
    server = smtplib.SMTP_SSL('smtp.yandex.ru',465)
    #server.starttls()
    server.connect('smtp.yandex.ru',465)
    server.login('o0oo.1111@yandex.ru', 'awyefslehqaiewph')
    # server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.send_message(msg)
    server.quit()

    return True
