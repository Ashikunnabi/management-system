from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from helper.permission import UserAccessApiBasePermission
from helper.viewset import CustomViewSet
from .serializers import *
from helper.helper import *

from account.models import User

            
@api_view(['POST'])
def registration(request):
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

    
@api_view(['POST'])
def check_username_existence(request):
    param = request.data
    required_params = ['username']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({0:"HELP: '{}' required.".format(error_param)}, status=400)
    
    user = User.objects.filter(username=param['username'])
    
    if user.exists():
        return Response({0:"HELP: '{}' already exists.".format(param['username'])}, status=405)
    else:
        return Response({0:"Valid username."}, status=200)   

    
@api_view(['POST'])
def check_email_existence(request):
    param = request.data
    required_params = ['email']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({0:"HELP: '{}' required.".format(error_param)}, status=400)
    
    user = User.objects.filter(email=param['email'])
    
    if user.exists():
        return Response({0:"HELP: '{}' already exists.".format(param['email'])}, status=405)
    else:
        return Response({0:"Valid email."}, status=200)
   
   
@api_view(['GET'])
def active_user(reuqest, activation_url):
    try:
        user = User.objects.get(
            user__is_active=False,
            activation_url=activation_url
        )
        user.is_active = True
        user.save()
        return Response({0:"Account activated"}, status=200)
    except:
        return Response({0:"Invalid Action"}, status=400)
 
 
@api_view(['GET'])
def reset_password_send_url(reuqest):
    param = request.data
    required_params = ['username']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({0:"HELP: '{}' required.".format(error_param)}, status=400)
    try: 
        user = User.objects.get(username=param.get('username'))
        account_activation_url = user.activation_url
        # send and email with profile_activation_url
    except:
        return Response({0:"Not an associate user."}, status=400)
 
 
@api_view(['POST'])
def reset_password(reuqest, activation_url):
    param = request.data
    required_params = ['password1', 'password2']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({0:"HELP: '{}' required.".format(error_param)}, status=400)
    
    if param['password1'] == param['password2']:
        try:
            user = User.objects.get(activation_url=activation_url)
            user.set_password(password1)
            user.save()
        except:
            return Response({0:"Invalid action"}, status=400)
    else:
        return Response({0:"Password does not matched."}, status=400)

def login(reuqest):
    pass
    

def logout(reuqest):
    pass
 
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(reuqest):
    param = reuqest.data
    required_params = ['username']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({0:"HELP: '{}' required.".format(error_param)}, status=400)  
    
    
    user = User.objects.filter(username=param['username'])[0]
    
    response = {
      'username': user.username,
      'email': user.email,
      'role': user.role.id,
      'permissions': [_.id for _ in user.role.permission.all()],
      'is_admin': user.is_superuser,
      'is_active': user.is_active,
    }
    return Response(response, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def make_admin(reuqest):
    params = request.data
    required_params = ['username', 'secret_code']
    
    # validating post data
    error_param = json_parameter_validation(params, required_params)
    if error_param is not None:
        return Response({0:"HELP: '{}' required.".format(error_param)}, status=400)
        
    if params.get('secret_code') != settings.SECRET_CODE_ADMIN:
        return Response({0:"You are not allowed to be an admin"}, status=401)
      
    # creating new user
    with transaction.atomic():
        user = User.objects.get(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.save()
    
    # send email with activation url
    
    return Response({0:"{} is now admin.".format(username)}, 200) 


class UserViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    model = User
    
    
    
class PermissionViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    model = Permission
 


class RoleViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    model = Role


















    