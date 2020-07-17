import json, requests
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.db import transaction
from django.shortcuts import redirect, reverse, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.core.rbac.permission import UserAccessApiBasePermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.core.rbac.utils import *
from apps.core.rbac.viewset import CustomViewSet
from .serializers import *  
from apps.core.rbac.models import *
from rest_framework_datatables import pagination as dt_pagination
from rest_framework.authentication import get_authorization_header


def store_user_activity(request, store_json='', description=''):
    ActivityLog.objects.create(store_json=store_json, description=description, 
                                ip_address=get_user_ip_address(request), browser_details=get_user_browser_details(request))
    return True

            
@api_view(['POST'])
def registration(request):
    required_params = ['first_name', 'last_name', 'username', 'email', 'password', 'is_active']
    params = request.data
    
    # validating post data
    if params.get('is_admin') is True:
        required_params.append('secret_code')
    error_param = json_parameter_validation(params, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)
        
    if params.get('is_admin') is True:
        if params.get('secret_code') == settings.SECRET_CODE_ADMIN:
            params['is_staff'] = True
            params['is_superuser'] = True
            del params['is_admin']
            del params['secret_code']
        else:
            return Response({"details": "You are not allowed to be an admin"}, status=401)
        
    # creating new user
    with transaction.atomic():
        user = User.objects.create_user(**params)
    
    # send email with activation url

    return Response({"details": "Registration Successful"}, status=201)    

    
@api_view(['GET'])
def check_username_existence(request):
    param = request.data
    required_params = ['username']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)
    
    user = User.objects.filter(username=param['username'])
    
    if user.exists():
        return Response({"details": "'{}' already exists.".format(param['username'])}, status=405)
    else:
        return Response({"details": "Valid username."}, status=200)   

    
@api_view(['GET'])
def check_email_existence(request):
    param = request.data
    required_params = ['email']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)
    
    user = User.objects.filter(email=param['email'])
    
    if user.exists():
        return Response({"details": "'{}' already exists.".format(param['email'])}, status=405)
    else:
        return Response({"details": "Valid email."}, status=200)
   
   
@api_view(['GET'])
def active_user(request, activation_url):
    try:
        user = User.objects.get(activation_url=activation_url)
        if user.is_active:
            return Response({"details": "Already account activated"}, status=200)
        user.is_active = True
        user.save()
        return Response({"details": "Account activated"}, status=200)
    except:
        return Response({"details": "Invalid Action"}, status=400)
 
 
@api_view(['GET'])
def reset_password_send_url(request):
    param = request.data
    required_params = ['username']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)
    try: 
        user = User.objects.get(username=param.get('username'))
        account_activation_url = user.activation_url
        # send and email with profile_activation_url
        return Response({"activation_url": account_activation_url}, status=200)
    except:
        return Response({"details": "Not an associate user."}, status=400)
 
 
@api_view(['POST'])
def reset_password(request, activation_url):
    param = request.data
    required_params = ['password1', 'password2']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)
    
    if param['password1'] == param['password2']:
        try:
            user = User.objects.get(activation_url=activation_url)
            user.set_password(password1)
            user.save()
        except:
            return Response({"details": "Invalid action"}, status=400)
    else:
        return Response({"details": "Password does not matched."}, status=400)
        

@api_view(['POST'])
def login(request):
    param = request.data
    required_params = ['username', 'password']    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)
    
    url = f"{request.build_absolute_uri().split('/api')[0]}{reverse('core:rbac:token_obtain_pair')}"
    token = requests.post(url, json=param)
    if token.status_code == 200:
        # activating session based authentication
        user = authenticate(username=request.data['username'], password=request.data['password'])
        auth_login(request, user)
        # storing user activity in ActivityLog
        user = User.objects.get(username=request.data['username'])
        store_user_activity(
            request,
            UserSerializer(user).data, 
            f'{user.get_full_name()}({user.username}) logged in successfully.'
        )
    return Response(token.json(), status=token.status_code)
    
    
@api_view(['GET'])
def logout(request):
    pass
 
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    param = request.data
    required_params = ['username']
    
    # validating data
    error_param = json_parameter_validation(param, required_params)
    if error_param is not None:
        return Response({"details": "'{}' required.".format(error_param)}, status=400)  
    
    
    user = User.objects.filter(username=param['username'])[0]
    
    response = {
      'username': user.username,
      'email': user.email,
      'role': user.role.id,
      'permissions': [_.id for _ in user.role.permission.all()],
      'is_admin': True if user.role.code in ['super_admin', 'admin'] else False,
      'is_active': user.is_active,
    }
    return Response(response, status=200)
 

class CustomerViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    model = Customer
 

class DomainViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()
    model = Domain
    

class TenantViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = TenantSerializer
    queryset = Domain.objects.all()
    model = Domain
 

class SidebarViewSet(viewsets.ModelViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    render_class = None
    pagination_class = None
    model = Feature
 

class FeatureViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    model = Feature

    
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


class GroupViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    model = Group
    

class UserViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    model = User 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')
        
    def destroy(self, request, pk=None):
        """ User can not be deleted. """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        
        if request.user.role.id == 1:
            user.delete()
            return Response({'details': 'User has been deleted successfully.'})
        else:
            user.is_active=False
            user.save()
            return Response(UserSerializer(user).data)
    


















