from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from apps.core.rbac.permission import UserAccessApiBasePermission
from apps.core.rbac.viewset import CustomViewSet
from apps.inventory.api.v1.serializers import *
from apps.inventory.models import *


class Category(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category
    name = 'category-detail'


class Product(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    model = Product
    name = 'product-detail'


class Vendor(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    model = Vendor
    name = 'vendor-detail'


class Customer(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    model = Customer
    name = 'customer-detail'

