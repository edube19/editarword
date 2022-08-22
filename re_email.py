from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def enviar_email(to, subject, message_text):
  CLIENT_SECRET_FILE = "./resources/credentials_oauth.json"
  API_NAME = "gmail"
  API_VERSION = "v1"
  SCOPES = ["https://mail.google.com/"]

  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
  message = MIMEMultipart()
  message['to'] = to
  message['subject'] = subject

  message.attach(MIMEText(message_text))

  raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()
  mensaje = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
  return print("Mensaje Enviado")