import requests
from django.shortcuts import render, redirect, reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def handler400(request, *args, **argv):
    return render(request, 'base/handle_errors/400.html')


def handler403(request, *args, **argv):
    return render(request, 'base/handle_errors/403.html')


def handler404(request, *args, **argv):
    return render(request, 'base/handle_errors/404.html')


def handler500(request, *args, **argv):
    return render(request, 'base/handle_errors/500.html')
    

def dashboard(request):
    return render(request, 'base/dashboard.html')


@api_view(['get'])
def sidebar(request):
    current_url = request.GET.get('current_url')
    url = f"{request.scheme}://{request.get_host()}/api/v1/sidebar/"
    response = requests.get(url, headers=request.headers).json()
    rearranged_list = []
    rearranged_dict = dict()
    
    for value in response:
        if value["parent"] is None:
            level_1 = []
            for v in response:
                if v["parent"] == str(value["id"]):
                    if current_url is not None and current_url == v["url"]:
                        v["status"] = True
                    level_1.append(v)
            value['level_1'] = level_1
            rearranged_list.append(value)
    return Response(rearranged_list, status=200)
    
    