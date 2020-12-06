from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout as auth_logout
from django.conf import settings


def registration(request):
    return render(request, 'rbac/registration.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return render(request, 'rbac/login.html')


def logout(request):    
    auth_logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


def reset(request):
    return render(request, 'rbac/reset.html')


def change_password(request):
    return render(request, 'rbac/change_password.html')
    
    
def permission(request):
    return render(request, 'rbac/permission.html')
    
    
def permission_add(request):
    return render(request, 'rbac/permission_add.html')
    
    
def permission_edit(request, id):
    return render(request, 'rbac/permission_edit.html', context={'id': id})
    
    
def role(request):
    return render(request, 'rbac/role.html')


def role_add(request):
    return render(request, 'rbac/role_add.html')


def role_edit(request, id):
    return render(request, 'rbac/role_edit.html', context={'id': id})
    
    
def group(request):
    return render(request, 'rbac/group.html')


def group_add(request):
    return render(request, 'rbac/group_add.html')


def group_edit(request, id):
    return render(request, 'rbac/group_edit.html', context={'id': id})
    
    
def user(request):
    return render(request, 'rbac/user.html')
    
    
def user_add(request):
    return render(request, 'rbac/user_add.html')
    
    
def user_edit(request, id):
    return render(request, 'rbac/user_edit.html', context={'id': id})
    
    
def customer(request):
    return render(request, 'rbac/customer.html')
    
    
def feature(request):
    return render(request, 'rbac/feature.html')


def branch(request):
    return render(request, 'rbac/branch.html')
