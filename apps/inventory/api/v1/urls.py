from django.urls import path, include
from rest_framework import routers
from .viewsets import *


router = routers.DefaultRouter()
router.register('category', Category)
router.register('product', Product)
router.register('vendor', Vendor)
router.register('customer', Customer)


urlpatterns = [
    path('', include(router.urls)),
]
