import smtplib
from email.mime.text import MIMEText
from flask import current_app

def send_email(name, otp, to_email):
  """ Send a password recovery email """
  
  msg = MIMEText(f"<html><body><table style='background: rgba(31, 30, 30, 0.034);' width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center'><table style='max-width: 35rem;' border='0' cellspacing='0' cellpadding='0'><tr><td style='background: black; padding: 1rem;'><h1 style='color: white; font-weight: bold; margin: 0;'>Reset password</h1></td></tr><tr><td style='background: white; color: black; padding-top: 2rem; padding-bottom: 2rem;'><table style='padding: 1rem;' border='0' cellspacing='0' cellpadding='0' width='100%'><tr><td><h2 style='margin-top: 0;'>Hello, {name}</h2><p style='font-size: 14px; margin-bottom: 0;'>We received a request to reset your password from your account. Enter the following code to reset the password:<br /><br /><span style=' font-size: 24px; font-weight: bold;'>{otp}</span></p><br /><br /></td></tr></table></td></tr><tr><td style='background: black; padding: 1rem;'><span style='color: white;  font-size: 12px; font-weight: bold;'>© 2025 DevGustavo All rights reserved</span></td></tr></table></td></tr></table></body></html>", 'html')
  msg["Subject"] = "Verification Code"
  msg["From"] = current_app.config['EMAIL_FROM']
  msg["To"] = to_email

  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(current_app.config['EMAIL_FROM'], current_app.config['EMAIL_PASSWORD'])  
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
  