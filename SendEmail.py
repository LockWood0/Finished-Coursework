import code
import os
import smtplib


def sendEmail(code, recipient):
    EMAIL_ADDRESS = "louis.cutteridge@gmail.com"
    EMAIL_PASSWORD = "cM8NzQjh!"

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = "Verification Code"
        body = "Here is your verification code: " + code

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADDRESS, recipient, msg)
    