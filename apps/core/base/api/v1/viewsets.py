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

            
@api_view(['POST'])
def test(request):
    required_params = ['first_name', 'last_name', 'username', 'email', 'password', 'is_active']
    params = request.data
    
    # validating post data
    if params.get('is_admin') is True:
        required_params.append('secret_code')
    error_param = json_parameter_validation(params, required_params)
    if error_param is not None:
        return Response({0:"'{}' required.".format(error_param)}, status=400)
        
    if params.get('is_admin') is True:
        if params.get('secret_code') == settings.SECRET_CODE_ADMIN:
            params['is_staff'] = True
            params['is_superuser'] = True
            del params['is_admin']
            del params['secret_code']
        else:
            return Response({0:"You are not allowed to be an admin"}, status=401)
        
    # creating new user
    with transaction.atomic():
        user = User.objects.create_user(**params)
    
    # send email with activation url
    
    return Response({0:"Registration Successful"}, status=201)    

    









    