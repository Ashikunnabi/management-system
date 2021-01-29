import requests
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.db import transaction
from django.shortcuts import reverse, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.base.custom_pagination import LargeResultsSetPagination
from apps.core.base.utils.basic import *
from apps.core.rbac.models import *
from apps.core.rbac.permission import UserAccessApiBasePermission
from apps.core.rbac.viewset import CustomViewSet
from .serializers import *


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
            user.set_password(param['password1'])
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
    pagination_class = LargeResultsSetPagination
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    model = Customer
    search_keywords = []
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class DomainViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()
    model = Domain
    search_keywords = []
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class TenantViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = TenantSerializer
    queryset = Domain.objects.all()
    model = Domain
    search_keywords = []
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class SidebarViewSet(viewsets.ModelViewSet):
    permission_classes = [UserAccessApiBasePermission]
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    render_class = None
    pagination_class = None
    model = Feature
    search_keywords = []
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class FeatureViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    model = Feature
    search_keywords = []
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class PermissionViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    model = Permission
    search_keywords = ['name', 'feature__title']
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class RoleViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    model = Role
    search_keywords = ['name']
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class GroupViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    model = Group
    search_keywords = ['name']
    # lookup_field = 'hashed_id'  # Individual object will be found by this field


class BranchViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    model = Branch
    search_keywords = ['name', 'address']
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        """ Create a new Branch and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Branch: A new Branch '{request.data.get('name')}' added.")

    def perform_update(self, instance, serializer, request):
        """ Update an existing Branch and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Branch: An existing Branch '{previous_data_before_update.name}' modified.")

    def perform_destroy(self, instance, request):
        """ Delete an existing Branch and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Branch: An existing branch '{serializer.get('name')}' deleted.")
        instance.delete()

    def validate_branch(self, name, parent):
        """
            Check duplication of the same branch
        :param name: branch name
        :param parent: branch parent (base branch)
        """
        branches = Branch.objects.filter(name__iexact=name)
        if not parent:
            if branches.filter(parent=None).count():
                raise serializers.ValidationError('Branch with this name already exists.')
        else:
            if branches.filter(parent__hashed_id=parent).count():
                raise serializers.ValidationError('Sub Branch with this name already exists in this Base branch.')

    def update_branch_path_on_parent_edit(self, instance, previous_path):
        if Branch.objects.filter(parent=instance.id).exists():
            have_to_change_branch_path = Branch.objects.filter(path__icontains=previous_path)
            for branch in have_to_change_branch_path:
                if instance.path == '/':
                    branch.path = branch.path.replace(previous_path, f"/{instance.name}")
                else:
                    branch.path = branch.path.replace(previous_path, instance.path)
            Branch.objects.bulk_update(have_to_change_branch_path, ['path'])

    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        name = request.data.get('name')
        # branch = request.data.get('branch')
        branch = request.data.get('parent')
        group = request.data.get('group')
        parent = request.data.get('parent')

        """ Duplicate branch name is not allowed."""
        self.validate_branch(name, parent)

        try:
            if parent:
                # Getting 'branch' object as parent and set it to 'parent' field
                existing_branch = get_object_or_404(Branch, hashed_id=parent)
                request.data.update({"parent": existing_branch.id})  # updating parent value null to given branch
            if group:
                # Using list comprehension as group is in manytomany relationship with branch
                existing_group = [get_object_or_404(Group, hashed_id=group).id for group in group]
                request.data.update({"group": existing_group})
        except Exception as ex:
            # if branch (optional), is not found then do not process request further
            title = ex.__str__().split(' ')[1].lower()  # # The exception is: No Group matches the given query..
            # from this we are taking Branch or Group
            return Response({title: ["Not Found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        name = request.data.get('name')
        # branch = request.data.get('parent')
        parent = request.data.get('parent')
        group = request.data.get('group')
        selected_branch = Branch.objects.get(hashed_id=kwargs.get('hashed_id'))

        # self.branch_name_validation(name)
        """ Duplicate branch name is not allowed."""
        if name or parent:
            self.validate_branch(name, parent)

        try:
            if parent:
                existing_branch = get_object_or_404(Branch, hashed_id=parent)
                request.data.update(
                    {"parent": existing_branch.id})  # updating the parent field value with given branch value
            if group:
                # Using list comprehension as group is in manytomany relationship with branch
                existing_group = [get_object_or_404(Group, hashed_id=group).id for group in group]
                request.data.update({"group": existing_group})
        except Exception as ex:
            # if branch or group is not found then do not process request further
            title = ex.__str__().split(' ')[
                1].upper()  # The exception is: The exception is: No Group/Branch matches the given query..
            # from this we are taking Category or Vendor or UnitType
            return Response({title: ["Not Found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        previous_path = instance.path
        if previous_path == '/':
            # if the branch is root then the path is '/'. That's why we are passing previous_path = /branch name
            previous_path = f"/{instance.name}"

        serializer = self.serializer_class(instance,
                                           data=request.data,
                                           partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            if previous_path != instance.path:
                self.update_branch_path_on_parent_edit(instance, previous_path)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Branch deleted successfully"}, status=status.HTTP_200_OK)


class DepartmentViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    model = Department
    search_keywords = []
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        """ Create a new Department and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Department: A new department '{request.data.get('name')}' added.")

    def perform_update(self, instance, serializer, request):
        """ Update an existing department and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Department: An existing department '{previous_data_before_update.name}' modified.")

    def perform_destroy(self, instance, request):
        """ Delete an existing department and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Department: An existing department '{serializer.get('name')}' deleted.")
        instance.delete()

    def validate_department(self, name, parent):
        """
            Check duplication of the same branch
        :param name: department name
        :param parent: department parent (base branch)
        """
        departments = Department.objects.filter(name__iexact=name)
        if not parent:
            if departments.filter(parent=None).count():
                raise serializers.ValidationError('Department with this name already exists.')
        else:
            if departments.filter(parent__hashed_id=parent).count():
                raise serializers.ValidationError('Sub Department with this name already exists in this Base '
                                                  'department.')

    def create(self, request, *args, **kwargs):
        """ Create a new department """

        name = request.data.get('name')
        # branch = request.data.get('branch')
        # parent_department = request.data.get('department')
        group = request.data.get('group')
        parent = request.data.get('parent')

        """ Duplicate department name is not allowed."""
        self.validate_department(name, parent)

        try:
            if parent:
                # Getting 'department' object as parent and set it to 'parent' field
                existing_department = get_object_or_404(Department, hashed_id=parent)
                request.data.update(
                    {"parent": existing_department.id})  # updating parent value null to given department
            if group:
                # Using list comprehension as group is in manytomany relationship with department
                existing_group = [get_object_or_404(Group, hashed_id=group).id for group in group]
                request.data.update({"group": existing_group})
            branch = get_object_or_404(Branch, hashed_id=request.data.get('branch'))
            request.data.update({"branch": branch.id})
        except Exception as ex:
            # if department (optional), is not found then do not process request further
            title = ex.__str__().split(' ')[1].lower()  # # The exception is: No Group matches the given query..
            # from this we are taking Department or Group
            return Response({title: ["Not Found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        try:
            if request.data.get('department'):
                department = get_object_or_404(Department, hashed_id=request.data.get('department'))
                request.data.update({"parent": department.id})  # Changing the department value hashed_id to id
            if request.data.get('group'):
                group = [get_object_or_404(Group, hashed_id=group).id for group in request.data.get('group')]
                request.data.update({"group": group})
            if request.data.get('branch'):
                branch = get_object_or_404(Branch, hashed_id=request.data.get('branch'))
                request.data.update({"branch": branch.id})  # changing the branch hashed_id to id
        except Exception as ex:
            # if department, group, branch is not found then don't process request further.
            title = ex.__str__().split(' ')[
                1].lower()  # The exception is: No Department/Group/Branch matches the given query..
            return Response({title: ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # Get the requested object instance
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  # validate posted data using serializer

        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"Detail": "Department deleted successfully."}, status=status.HTTP_200_OK)


class UserViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    pagination_class = LargeResultsSetPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()
    model = User
    search_keywords = ['username', 'first_name', 'last_name', 'position', 'email']

    # lookup_field = 'hashed_id'  # Individual object will be found by this field

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
            user.is_active = False
            user.save()
            return Response(UserSerializer(user).data)
