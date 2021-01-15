from apps.core.base.utils.basic import store_user_activity
from apps.core.rbac.permission import UserAccessApiBasePermission
from apps.core.rbac.viewset import CustomViewSet
from apps.inventory.api.v1.serializers import *
from apps.inventory.models import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class CategoryViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category
    # Individual object will be found by this field. 
    lookup_field = 'hashed_id'

    def perform_create(self, serializer, request):
        """ Create a new category and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Category: A new category "
                            f"'{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an existing category and store activity log. """
        previous_data_before_update = self.model.objects.get(
            hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Category: An existing category "
                            f"'{previous_data_before_update.name}' modified."
                            )

    def perform_destroy(self, instance, request):
        """ Delete an existing category and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Category: An existing category "
                            f"'{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        parent = request.data.get('parent')
        department = request.data.get('department')
        try:
            if parent:
                # Getting 'category' as parent obj and set it to 'parent' field
                category = get_object_or_404(
                    Category,
                    hashed_id=parent
                )
                # updating parent field value null to given category
                request.data.update(
                    {
                        "parent": category.id
                    }
                )

            department_obj = get_object_or_404(
                Department,
                hashed_id=department
            )
            # Changing the value of dep value, hashed_id to id of json. 
            # So that other relational operation can be done by id 
            # which is default.
            request.data.update(
                {
                    "department": department_obj.id
                }
            )
        except Exception as ex:
            # if category (optional), department is not found then 
            # do not process request further
            # The exception is: No Category/Department found.
            title = ex.__str__().split(' ')[1].lower()  
            # from this we are taking Category or Department
            return Response({title: ["Not found."]}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # validate posted data using serializer
        serializer = self.serializer_class(data=request.data)  
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        parent = request.data.get('parent')
        department = request.data.get('department')
        try:
            if parent:
                # Getting 'category' as parent obj and set it to 'parent' field
                category = get_object_or_404(
                    Category,
                    hashed_id=parent
                )
                # updating parent field value null to given category
                request.data.update(
                    {
                        "parent": category.id
                    }
                )

            department_obj = get_object_or_404(
                Department,
                hashed_id=department
            )
            # Changing the value of dep value, hashed_id to id of json.
            # So that other relational operation can be done by id
            # which is default.
            request.data.update(
                {
                    "department": department_obj.id
                }
            )
        except Exception as ex:
            # if category (optional), department (optional) 
            # is not found then do not process request further 
            # The exception is: No Department/Category matches the given query.
            # from this we are taking Category or Department
            title = ex.__str__().split(' ')[1].lower() 
            return Response({title: ["Not found."]}, 
                            status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        # validate posted data using serializer
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Category deleted successfully"}, 
                        status=status.HTTP_200_OK)


class JsTreeCategoryViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Category.objects.all()
    serializer_class = JsTreeCategorySerializer
    model = Category
    # Individual object will be found by this field.
    lookup_field = 'hashed_id'
    http_method_names = ['get']

    def get_queryset(self):
        category_hashed_id = self.request.GET.get('id')

        if self.request.GET.get('id') == '#':
            # for root category there is no parent
            queryset = self.queryset.filter(parent_id=None)
        else:

            queryset = self.queryset.filter(
                parent_id=self.queryset.get(hashed_id=category_hashed_id).id
            )
        return queryset


class VendorViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    model = Vendor
    # Individual object will be found by this field.
    lookup_field = 'hashed_id'  

    def perform_create(self, serializer, request):
        """ Create a new vendor and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Vendor: A new vendor "
                            f"'{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an existing vendor and store activity log. """
        previous_data_before_update = self.model.objects.get(
            hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Vendor: An existing vendor "
                            f"'{previous_data_before_update.name}' modified."
                            )

    def perform_destroy(self, instance, request):
        """ Delete an existing vendor and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Vendor: An existing vendor "
                            f"'{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            category = get_object_or_404(Category, 
                                         hashed_id=request.data.get('category')
                                         )
            # Changing the value of category value, hashed_id to id of json. 
            # So that other relational operation can be done by id 
            # which is default.
            request.data.update({"category": category.id})  
        except Exception as ex:
            # if category is not found then do not process request further
            return Response({"category": ["Not found."]}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
            # validate posted data using serializer
        serializer = self.serializer_class(data=request.data)  
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.data.get('category'):
            try:
                category = get_object_or_404(
                    Category, hashed_id=request.data.get('category')) 
                # Changing the value of category value, hashed_id to id of 
                # json. So that other relational operation can be done 
                # by id which is default.
                request.data.update({"category": category.id}) 
            except Exception as ex:
                # if category is not found then do not process request further
                return Response({"category": ["Not found."]}, 
                                status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        # validate posted data using serializer
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)  
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Vendor deleted successfully"}, 
                        status=status.HTTP_200_OK)


class UnitTypeViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    model = UnitType
    # Individual object will be found by this field
    lookup_field = 'hashed_id'

    def perform_create(self, serializer, request):
        """ Create a new unit type and store activity log. """
        serializer.save()

        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Unit Type: A new unit type "
                            f"'{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an existing unit type and store activity log. """
        previous_data_before_update = self.model.objects.get(
            hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Unit Type: An existing unit type "
                            f"'{previous_data_before_update.name}' modified."
                            )

    def perform_destroy(self, instance, request):
        """ Delete an existing unit type and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Unit Type: An existing unit type "
                            f"'{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        if request.data.get('category'):
            try:
                category = get_object_or_404(
                    Category, hashed_id=request.data.get('category'))
                # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be
                # done by id which is default.
                request.data.update({"category": category.id})
            except Exception as ex:
                # if category is not found then do not process request further
                return Response({"category": ["Not found."]},
                                status=status.HTTP_400_BAD_REQUEST)

        # validate posted data using serializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.data.get('category'):
            try:
                category = get_object_or_404(
                    Category, hashed_id=request.data.get('category'))
                # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be
                # done by id which is default.
                request.data.update({"category": category.id})
            except Exception as ex:
                # if category is not found then do not process request further
                return Response({"category": ["Not found."]},
                                status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()  # get the requested object instance
        # validate posted data using serializer
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Unit type deleted successfully"},
                        status=status.HTTP_200_OK)


class ProductViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    model = Product
    # Individual object will be found by this field
    lookup_field = 'hashed_id'

    def perform_create(self, serializer, request):
        """ Create a new product and store activity log. """
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Product: A new product "
                            f"'{request.data.get('name')}' added."
                            )

    def perform_update(self, instance, serializer, request):
        """ Update an existing product and store activity log. """
        previous_data_before_update = self.model.objects.get(
            hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Product: An existing product "
                            f"'{previous_data_before_update.name}' modified."
                            )

    def perform_destroy(self, instance, request):
        """ Delete an existing product and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Product: An existing product "
                            f"'{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            category = get_object_or_404(Category,
                                         hashed_id=request.data.get('category')
                                         )
            # Changing the value of category value, hashed_id to id
            # of json. So that other relational operation can be
            # done by id which is default.
            request.data.update({"category": category.id})
                #
            vendor = get_object_or_404(Vendor,
                                       hashed_id=request.data.get('vendor'))
            # Changing the value of vendor value, hashed_id to id of json.
            # So that other relational operation can be done by id
            # which is default.
            request.data.update({"vendor": vendor.id})
            unit_type = get_object_or_404(
                UnitType, hashed_id=request.data.get('unit_type'))
            # Changing the value of unit_type value, hashed_id to id of json.
            # So that other relational operation can be done by id
            # which is default.
            request.data.update({"unit_type": unit_type.id})
        except Exception as ex:
            # if category, vendor & unit_type is not found then do not
            # process request further The exception is: No
            # Category/Vendor/UnitType found from this we are taking
            # Category or Vendor or UnitType.
            title = ex.__str__().split(' ')[1].lower()
            # as model has the field like 'unit_type' that's why setting
            # title value = 'unit_type'
            title = 'unit_type' if title == 'unittype' else title
            return Response({title: ["Not found."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # validate posted data using serializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            if request.data.get('category'):
                category = get_object_or_404(
                    Category, hashed_id=request.data.get('category'))
                # Changing the value of category value, hashed_id to id
                # of json. So that other relational operation can be done
                # by id which is default.
                request.data.update({"category": category.id})
            if request.data.get('vendor'):
                vendor = get_object_or_404(
                    Vendor, hashed_id=request.data.get('vendor'))
                request.data.update({"vendor": vendor.id})
            if request.data.get('unit_type'):
                unit_type = get_object_or_404(
                    UnitType, hashed_id=request.data.get('unit_type'))
                request.data.update({"unit_type": unit_type.id})
        except Exception as ex:
            # if category, vendor, unit_type is not found then do not
            # process request further The exception is:
            # No Category/Vendor/UnitType found. from this we are taking
            # Category or Vendor or UnitType
            title = ex.__str__().split(' ')[1].lower()
            title = 'unit_type' if title == 'unittype' else title
            return Response({title: ["Not found."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # get the requested object instance
        instance = self.get_object()
        # validate posted data using serializer
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # get the requested object instance
        instance = self.get_object()
        self.perform_destroy(instance, request)
        return Response({"detail": "Unit type deleted successfully"},
                        status=status.HTTP_200_OK)


class CustomerViewSet(CustomViewSet):
    permission_classes = [UserAccessApiBasePermission]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    model = Customer
    # Individual object will be found by this field
    lookup_field = 'hashed_id'

    def perform_create(self, serializer, request):
        """ Create a new customer and store activity log. """
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Customer: A new customer "
                            f"'{request.data.get('name')}' added."
                            )
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing customer and store activity log. """
        previous_data_before_update = self.model.objects.get(
            hashed_id=instance.hashed_id)
        store_user_activity(request,
                            store_json=serializer.data,
                            description=f"Customer: An existing customer "
                            f"'{previous_data_before_update.name}' modified."
                            )
        serializer.save()

    def perform_destroy(self, instance, request):
        """ Delete an existing customer and store activity log. """
        serializer = self.serializer_class(instance).data
        store_user_activity(request,
                            store_json=serializer,
                            description=f"Customer: An existing customer "
                            f"'{serializer.get('name')}' deleted."
                            )
        instance.delete()

    def create(self, request, *args, **kwargs):
        # validate posted data using serializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        # validate posted data using serializer
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # get the requested object instance
        instance = self.get_object()
        self.perform_destroy(instance, request)
        return Response({"detail": "Customer deleted successfully"},
                        status=status.HTTP_200_OK)
