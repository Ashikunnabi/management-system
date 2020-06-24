from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *

from apps.core.rbac.models import User

            
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_balance(request):
    """
        Check total sms left in the API account

        :parameter
            None

        :return:
            json: list of parameters
                    - success (boolean): is data successfully retrieved
                    - message (string): response message
                    - response_code (int): response code
                    - available_sms (int): number of available sms left in the API Account
    """

    response = requests.get('{}g_api.php?token={}&totalsms'.format(settings.SMS_API_ENDPOINT, settings.SMS_API_TOKEN))
    text = response.text.split("<")[0]
    code = response.status_code

    data = {
        "response_code": code,
        "available_sms": text
    }

    return JsonResponse(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sms_charge(request):
    """
        Get sms charge for per sms

        :parameter
            None

        :return:
            json: list of parameters
                    - success (boolean): is data successfully retrieved
                    - message (string): response message
                    - response_code (int): response code
                    - sms_charge (string): per sms rate
    """

    response = requests.get('{}g_api.php?token={}&totalsms'.format(settings.SMS_API_ENDPOINT, settings.SMS_API_TOKEN))
    text = response.text.split("<")[0] + " BDT/per sms"
    code = response.status_code

    data = {
        "response_code": code,
        "sms_charge": text
    }
    return JsonResponse(data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_total_sms_sent(request):
    """
        Check total sms sent by this account so far

        :parameter
            None

        :return:
            json: list of parameters
                    - success (boolean): is data successfully retrieved
                    - message (string): response message
                    - response_code (int): response code
                    - sent_sms (int): number of sms sent by the account user
    """

    response = requests.get('{}g_api.php?token={}&totalsms'.format(settings.SMS_API_ENDPOINT, settings.SMS_API_TOKEN))
    text = response.text.split("<")[0]
    code = response.status_code

    data = {
        "response_code": code,
        "sent_sms": text
    }
    return JsonResponse(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_sms_expiry_date(request):
    """
        Check sms balance expiry date

        :parameter
            None

        :return:
            json: list of parameters
                    - success (boolean): is data successfully retrieved
                    - message (string): response message
                    - response_code (int): response code
                    - expiry_date (string): expiry date
    """

    response = requests.get('{}g_api.php?token={}&totalsms'.format(settings.SMS_API_ENDPOINT, settings.SMS_API_TOKEN))
    text = response.text.split("<")[0]
    code = response.status_code

    data = {
        "response_code": code,
        "expiry_date": text
    }
    return JsonResponse(data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_sms(request):
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
                                                     request.data['mobile_number'], request.data['message']))
    text = response.text.split("<")[0]
    code = response.status_code

    data = {
        "success": success,
        "message": message,
    }
    return JsonResponse(data)
    









    