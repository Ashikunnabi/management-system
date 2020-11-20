from django.conf import settings
from django.http import JsonResponse
import requests


def json_parameter_validation(json_data, required_params):
    """ Check parameter is available in json or not
        parameter:
        ---------
            json_data: dict, required
                A dictionary that should be validate by pramas are available or not
            required_params: list, required
                Those list of params that must be available on json_data
        return:
        ------
            required_params: list
                If required parameter is not in json_data then return that parameter name othrewise None
    """
    for param in required_params:
        if json_data.get(param) is None:
            return param
            

def get_user_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
            

def get_user_browser_details(request):    
    return request.headers.get('User-Agent')
            

def send_sms(request, mobile_number, message): 
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

    response = requests.post(
        '{}api.php?token={}&to={}&message={}'.format(settings.SMS_API_ENDPOINT, settings.SMS_API_TOKEN,
                                                     mobile_number, message))
    text = response.text.split("<")[0]
    code = response.status_code

    data = {
        "response_code": code,
        "sms_status": text
    }
    return JsonResponse(data)
    
    
