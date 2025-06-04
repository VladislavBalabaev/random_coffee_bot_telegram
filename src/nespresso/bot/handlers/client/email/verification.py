import logging
import secrets
from email.message import EmailMessage

import aiosmtplib

from nespresso.core.configs.settings import settings

_EMAIL_ADDRESS = settings.EMAIL_ADDRESS.get_secret_value()
_EMAIL_PASSWORD = settings.EMAIL_PASSWORD.get_secret_value()


_SMTP_HOST = "smtp.gmail.com"
_SMTP_PORT = 587


def CreateCode() -> int:
    return secrets.randbelow(900000) + 100000


async def SendCode(email: str, code: int) -> None:
    message = EmailMessage()

    message["Subject"] = "Verification code (NESpresso)"
    message["From"] = _EMAIL_ADDRESS
    message["To"] = email
    message.set_content(
        f"Hello,\n\nThank you for registering with the NESpresso Telegram bot!\nTo complete your registration, please use the verification code below:\n\nVerification Code: {code}\n\nIf you did not initiate this request, please disregard this email.\n\nBest regards,\nThe NESpresso Bot Team"
    )

    await aiosmtplib.send(
        message,
        username=_EMAIL_ADDRESS,
        password=_EMAIL_PASSWORD,
        hostname=_SMTP_HOST,
        port=_SMTP_PORT,
        start_tls=True,
    )

    logging.info(f"Sending code '{code}' to '{email}'")


# async def TestEmail() -> None:
#     logging.info("### Checking emails ... ###")

#     failed_emails = []

#     for email_sender in emails:
#         try:
#             message = EmailMessage()
#             message["Subject"] = "Проверка работоспособности (NEScafeBot)"
#             message["From"] = email_sender["email"]
#             message["To"] = "vbalabaev@nes.ru"
#             message.set_content("Почта работает.")


#             await aiosmtplib.send(
#                 message,
#                 username=email_sender["email"],
#                 password=email_sender["password"],
#                 hostname="smtp.gmail.com",
#                 port=587,
#                 start_tls=True,
#             )

#         except SMTPAuthenticationError:
#             logging.warning(f"process='email test' !! Email \"{email_sender['email']}\" is not working.")

#             await send_to_admins(f"WARNING: Email \"{email_sender['email']}\" is not working")

#             failed_emails.append(email_sender)

#     for email_sender in failed_emails:
#         emails.remove(email_sender);

#     logging.info("### Emails have been checked! ###")
