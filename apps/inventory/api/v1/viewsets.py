from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, pagination

from apps.core.rbac.permission import UserAccessApiBasePermission
from apps.core.rbac.viewset import CustomViewSet
from apps.inventory.api.v1.serializers import *
from apps.inventory.models import *
from django.shortcuts import get_object_or_404
from apps.core.base.utils.basic import store_user_activity


class CategoryViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        """ Create a new category and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Category: A new category '{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an exidting category and store activity log. """
        previous_data_before_update = Category.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Category: An existing category '{previous_data_before_update.name}' modified."
                            )

    def perform_destroy(self, instance, request):
        """ Delete an existing category and store activity log. """
        serializer = CategorySerializer(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Category: An existing category '{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            department = get_object_or_404(Department, hashed_id=request.data.get('department'))
            request.data.update({"department": department.id})
        except Exception as ex:
            # if department is not found then do not process request further
            return Response({"department": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.data.get('department'):
            try:
                department = get_object_or_404(Department, hashed_id=request.data.get('department'))
                request.data.update({"department": department.id})
            except Exception as ex:
                # if department is not found then do not process request further
                return Response({"department": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        serializer = self.serializer_class(instance, data=request.data, partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({'Category deleted successfully'}, status=status.HTTP_200_OK)


class VendorViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    model = Vendor
    lookup_field = 'hashed_id'  # Individual object will be found by this field


class UnitTypeViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    model = UnitType
    lookup_field = 'hashed_id'  # Individual object will be found by this field


class ProductViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    model = Product
    lookup_field = 'hashed_id'  # Individual object will be found by this field
    # pagination.PageNumberPagination.page_size = 0  #


class CustomerViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    model = Customer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

