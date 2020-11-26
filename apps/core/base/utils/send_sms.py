import logging
import requests
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger('django')


def send_sms(mobile_number, message):
    """
        Send sms to specific phone number

        :parameter
            phone_no (string): phone number to send sms
            message (string): message to send

        :return:
            json: list of parameters
                    - success (boolean): is data successfully retrieved
                    - message (string): response message
                    - response_code (int): response code
                    - sms_status (string): message sending status
    """
    try:
        response = requests.post(
            '{}api.php?token={}&to={}&message={}'.format(settings.SMS_API_ENDPOINT,
                                                         settings.SMS_API_TOKEN,
                                                         mobile_number, message))
        text = response.text.split("<")[0]
        code = response.status_code
        data = {
            "response_code": code,
            "sms_status": text
        }
        logger.info(response + '\n\n')
        return JsonResponse(data)
    except Exception as ex:
        logger.error(ex.__str__() + '\n\n')
        return JsonResponse(ex.__str__())
