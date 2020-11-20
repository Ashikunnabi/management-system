from django.core.mail import send_mail
from django.conf import settings
from .basic import logger_info, logger_error


def simple_email(subject: str, body: str, to: list = []) -> str:
    """
        Send email to list of user

        :parameter
            subject (string): Email subject
            body (string): Email body only text
            to (list): list of recipient

        :return:
            str: a success message or an error message
    """
    if subject == '':
        return 'Please provide subject as it is mandatory.'
    if len(to) < 1:
        return 'Please provide whom to send email. Example to=["abc@abc.com"].'

    try:
        send_mail(subject, body, settings.EMAIL_HOST, to, fail_silently=False)
        response = f'Mail send successfully at {to}'
        logger_info(response)
        return response
    except Exception as ex:
        logger_error(ex.__str__())
        return ex.__str__()
