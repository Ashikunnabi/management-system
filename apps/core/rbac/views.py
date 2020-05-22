from django.shortcuts import render, redirect



def registration(request):
    return render(request, 'rbac/registration.html')


def login(request):
    return render(request, 'rbac/user.html')


def logout(request):
    return redirect('login')


def reset(request):
    return render(request, 'rbac/reset.html')


def change_password(request):
    return render(request, 'rbac/change_password.html')
    
    
def permission(request):
    return render(request, 'rbac/permission.html')
    
    
def role(request):
    return render(request, 'rbac/role.html')
    
    
def user(request):
    return render(request, 'rbac/user.html')
    
    
def customer(request):
    return render(request, 'rbac/customer.html')
    
    
def feature(request):
    return render(request, 'rbac/feature.html')
