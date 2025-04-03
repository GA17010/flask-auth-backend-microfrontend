import smtplib
from email.mime.text import MIMEText
from flask import current_app

def send_email(name, otp, to_email):
  """ Envía un correo de recuperación de contraseña """
  
  msg = MIMEText(f"<html><body><table style='background: rgba(31, 30, 30, 0.034);' width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center'><table style='max-width: 35rem;' border='0' cellspacing='0' cellpadding='0'><tr><td style='background: black; padding: 1rem;'><h1 style='color: white; font-weight: bold; margin: 0;'>Restablecer la contraseña</h1></td></tr><tr><td style='background: white; color: black; padding-top: 2rem; padding-bottom: 2rem;'><table style='padding: 1rem;' border='0' cellspacing='0' cellpadding='0' width='100%'><tr><td><h2 style='margin-top: 0;'>Hola, {name}</h2><p style='font-size: 14px; margin-bottom: 0;'>Recibimos una solicitud para restablecer tu contraseña de su cuenta. Ingresa el siguiente código para restablecer la contraseña:<br /><br /><span style=' font-size: 24px; font-weight: bold;'>{otp}</span></p><br /><br /></td></tr></table></td></tr><tr><td style='background: black; padding: 1rem;'><span style='color: white;  font-size: 12px; font-weight: bold;'>© 2025 DevGustavo Todos los derechos reservados</span></td></tr></table></td></tr></table></body></html>", 'html')
  msg["Subject"] = "Restablecer contraseña"
  msg["From"] = current_app.config['EMAIL_FROM']
  msg["To"] = to_email

  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(current_app.config['EMAIL_FROM'], current_app.config['EMAIL_PASSWORD'])  
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
  