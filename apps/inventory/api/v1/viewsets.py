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
    lookup_field = 'hashed_id'  # Individual object will be found by this field. Doing this for security purpose.

    # pagination.PageNumberPagination.page_size = 0  # get all objects in response

    def perform_create(self, serializer, request):
        """ Create a new category and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Category: A new category '{request.data.get('name')}' added."
                            )


    def perform_update(self, instance, serializer, request):
        """ Update an existing category and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Category: An existing category '{previous_data_before_update.name}' modified."
                            )


    def perform_destroy(self, instance, request):
        """ Delete an existing category and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Category: An existing category '{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            if request.data.get('category'):
                # Getting 'category' as parent obj and set it to 'parent' field
                category = get_object_or_404(Category, hashed_id=request.data.get('category'))
                request.data.update({"parent": category.id})  # Changing the value of category value hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            department = get_object_or_404(Department, hashed_id=request.data.get('department'))
            request.data.update({"department": department.id})  # Changing the value of dep value, hashed_id to id
            # of json. So that other relational operation can be done by id which is default.
        except Exception as ex:
            # if category (optional), department is not found then do not process request further
            title = ex.__str__().split(' ')[1].lower()  # The exception is: No Category/Department found.
            # from this we are taking Category or Department
            return Response({title: ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            if request.data.get('category'):
                category = get_object_or_404(Category, hashed_id=request.data.get('category'))
                request.data.update({"parent": category.id})  # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done by using id which is default.
            if request.data.get('department'):
                department = get_object_or_404(Department, hashed_id=request.data.get('department'))
                request.data.update({"department": department.id})  # Changing the value of dep value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
        except Exception as ex:
            # if category (optional), department (optional) is not found then do not process request further
            title = ex.__str__().split(' ')[1].lower()  # The exception is: 'No Category/Department found'.
            # from this we are taking Category or Department
            return Response({title: ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Category deleted successfully"}, status=status.HTTP_200_OK)


class VendorViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    model = Vendor
    lookup_field = 'hashed_id'  # Individual object will be found by this field.  Doing this for security purpose.

    # pagination.PageNumberPagination.page_size = 0  # get all objects in response

    def perform_create(self, serializer, request):
        """ Create a new vendor and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Vendor: A new vendor '{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an existing vendor and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Vendor: An existing vendor '{previous_data_before_update.name}' modified."
                            )


    def perform_destroy(self, instance, request):
        """ Delete an existing vendor and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Vendor: An existing vendor '{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            category = get_object_or_404(Category, hashed_id=request.data.get('category'))
            request.data.update({"category": category.id})  # Changing the value of category value, hashed_id to id
            # of json. So that other relational operation can be done by id which is default.
        except Exception as ex:
            # if category is not found then do not process request further
            return Response({"category": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.data.get('category'):
            try:
                category = get_object_or_404(Category, hashed_id=request.data.get('category'))
                request.data.update({"category": category.id})  # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            except Exception as ex:
                # if category is not found then do not process request further
                return Response({"category": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Vendor deleted successfully"}, status=status.HTTP_200_OK)


class UnitTypeViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    model = UnitType
    lookup_field = 'hashed_id'  # Individual object will be found by this field.  Doing this for security purpose.

    # pagination.PageNumberPagination.page_size = 0  # get all objects in response

    def perform_create(self, serializer, request):
        """ Create a new unit type and store activity log. """
        serializer.save()

        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Unit Type: A new unit type '{request.data.get('name')}' added."
                            )
    def perform_update(self, instance, serializer, request):
        """ Update an existing unit type and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Unit Type: An existing unit type '{previous_data_before_update.name}' modified."
                            )


    def perform_destroy(self, instance, request):
        """ Delete an existing unit type and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Unit Type: An existing unit type '{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        if request.data.get('category'):
            try:
                category = get_object_or_404(Category, hashed_id=request.data.get('category'))
                request.data.update({"category": category.id})  # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            except Exception as ex:
                # if category is not found then do not process request further
                return Response({"category": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.data.get('category'):
            try:
                category = get_object_or_404(Category, hashed_id=request.data.get('category'))
                request.data.update({"category": category.id})  # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            except Exception as ex:
                # if category is not found then do not process request further
                return Response({"category": ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Unit type deleted successfully"}, status=status.HTTP_200_OK)


class ProductViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    model = Product
    lookup_field = 'hashed_id'  # Individual object will be found by this field.  Doing this for security purpose.

    # pagination.PageNumberPagination.page_size = 0  # get all objects in response

    def perform_create(self, serializer, request):
        """ Create a new product and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Product: A new product '{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an existing product and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Product: An existing product '{previous_data_before_update.name}' modified."
                            )


    def perform_destroy(self, instance, request):
        """ Delete an existing product and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Product: An existing product '{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            category = get_object_or_404(Category, hashed_id=request.data.get('category'))
            request.data.update({"category": category.id})   # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            vendor = get_object_or_404(Vendor, hashed_id=request.data.get('vendor'))
            request.data.update({"vendor": vendor.id})   # Changing the value of vendor value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            unit_type = get_object_or_404(UnitType, hashed_id=request.data.get('unit_type'))
            request.data.update({"unit_type": unit_type.id})   # Changing the value of unit_type value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
        except Exception as ex:
            # if category, vendor & unit_type is not found then do not process request further
            title = ex.__str__().split(' ')[1].lower()  # The exception is: No Category/Vendor/UnitType found.
            # from this we are taking Category or Vendor or UnitType
            title = 'unit_type' if title == 'unittype' else title  # as model has the field like 'unit_type' that's why
            # setting title value = 'unit_type'
            return Response({title: ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            if request.data.get('category'):
                category = get_object_or_404(Category, hashed_id=request.data.get('category'))
                request.data.update({"category": category.id})   # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done by id which is default.
            if request.data.get('vendor'):
                vendor = get_object_or_404(Vendor, hashed_id=request.data.get('vendor'))
                request.data.update({"vendor": vendor.id})
            if request.data.get('unit_type'):
                unit_type = get_object_or_404(UnitType, hashed_id=request.data.get('unit_type'))
                request.data.update({"unit_type": unit_type.id})
        except Exception as ex:
            # if category, vendor, unit_type is not found then do not process request further
            title = ex.__str__().split(' ')[1].lower()   # The exception is: No Category/Vendor/UnitType found.
            # from this we are taking Category or Vendor or UnitType
            title = 'unit_type' if title == 'unittype' else title
            return Response({title: ["Not found."]}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Unit type deleted successfully"}, status=status.HTTP_200_OK)


class CustomerViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    model = Customer
    lookup_field = 'hashed_id'  # Individual object will be found by this field.  Doing this for security purpose.

    # pagination.PageNumberPagination.page_size = 0  # get all objects in response

    def perform_create(self, serializer, request):
        """ Create a new customer and store activity log. """
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Customer: A new customer '{request.data.get('name')}' added."
                            )
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing customer and store activity log. """
        previous_data_before_update = self.model.objects.get(hashed_id=instance.hashed_id)
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Customer: An existing customer '{previous_data_before_update.name}' modified."
                            )
        serializer.save()

    def perform_destroy(self, instance, request):
        """ Delete an existing customer and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Customer: An existing customer '{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  # validate posted data using serializer
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Customer deleted successfully"}, status=status.HTTP_200_OK)
