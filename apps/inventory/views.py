from django.shortcuts import render


def category(request):
    return render(request, 'inventory/category.html')
