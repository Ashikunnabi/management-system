from django.urls import path, include
from rest_framework import routers
from .viewsets import *


router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('js-tree-category', JsTreeCategoryViewSet)
router.register('vendor', VendorViewSet)
router.register('unit-type', UnitTypeViewSet)
router.register('product', ProductViewSet)
router.register('customer', CustomerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
