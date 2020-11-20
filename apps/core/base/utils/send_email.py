from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger('django')


class SendEmail:
    def __init__(self, subject: str, body: str, to: list) -> None:
        """
            Send email to list of user

            :parameter
                subject (string): Email subject
                body (string): Email body only text
                to (list): list of recipient

            :return:
                None
        """
        self.subject = subject
        self.body = body
        self.to = to

    def simple_email(self) -> str:
        """
            Send simple text email to list of user

            :parameter
                self (SendEmail): SendEmail objects instance

            :return:
                str: a success message or an error message
        """
        try:
            send_mail(self.subject, self.body, settings.EMAIL_HOST, self.to, fail_silently=False)
            response = f'Mail send successfully at {self.to}'
            logger.info(response + '\n\n')
            return response
        except Exception as ex:
            logger.error(ex.__str__() + '\n\n')
            return ex.__str__()

    def email_with_attachment(self, attachment_path) -> str:
        """
            Send email with attachment to list of user

            :parameter
                self (SendEmail): SendEmail objects instance

            :return:
                str: a success message or an error message
        """
        try:
            email = EmailMessage(
                subject=self.subject,
                body=self.body,
                from_email=settings.EMAIL_HOST,
                to=self.to,
                bcc=[],
                reply_to=[],
                headers={},
            )
            email.attach_file(attachment_path)
            email.send(fail_silently=False)
            response = f'Mail send successfully at {self.to}'
            logger.info(response + '\n\n')
            return response
        except Exception as ex:
            logger.error(ex.__str__() + '\n\n')
            return ex.__str__()
