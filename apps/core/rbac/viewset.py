import operator
from functools import reduce
from django.db.models import Q
from rest_framework import viewsets


class CustomViewSet(viewsets.ModelViewSet):
    model = None
    change_keys = None
    search_keywords = None
    queryset = None
    query = None

    def dt_search(self):
        search = self.request.query_params.get('search[value]', None)

        # search
        if search and search is not None and self.search_keywords is not None:
            search_logic = []

            for entity in self.search_keywords:
                search_logic.append(Q(**{entity + '__icontains': search}))

            self.query = self.query.filter(reduce(operator.or_, search_logic))

        return self.query

    # ascending or descending order
    def dt_order(self):
        column_id = self.request.query_params.get('order[0][column]', None)

        if column_id and column_id is not None:
            column_name = self.request.query_params.get(
                'columns[' + column_id + '][data]', None)

            if self.change_keys is not None:
                for key in self.change_keys:
                    if column_name == key:
                        column_name = self.change_keys.get(key)

            if column_name != '':
                order_dir = '-' if self.request.query_params.get(
                    'order[0][dir]') == 'desc' else ''
                self.query = self.query.order_by(order_dir + column_name)

        return self.query

                
    def get_queryset(self):
        if self.model is None:
            raise AssertionError('CustomViewSetForQuerySet need to include a model')
        self.query = self.object_level_permission()
        self.query = self.dt_search()
        self.query = self.dt_order()
        return self.query

    def get_permissions(self):
        for permission in self.permission_classes:
            if permission.__name__ == 'UserAccessApiBasePermission':
                return [permission(self.model)]
            else:
                return [permission()]

    # defining user can see what depending on role
    def object_level_permission(self):
        app_label = str(self.model._meta.app_label)
        object_class_name = str(self.model._meta.model_name)  
        app_label_class_name = app_label+ '_' + object_class_name
        queryset = self.model.objects.filter()
        
        if app_label_class_name in ['rbac_feature']:
            if self.request.user.role.code in ['super_admin']:
                queryset = self.model.objects.all()
            elif self.request.user.role.code in ['admin']:
                queryset = self.model.objects.filter(is_active=True)                
            else:
                # Other users can see those features that they got permission to view
                view_permissions = self.request.user.role.permission.filter(code__contains='view.').values_list('feature_id', flat=True)
                queryset = self.model.objects.filter(is_active=True, permission_feature__in=view_permissions)
        
        if app_label_class_name in ['rbac_customer']:
            if self.request.user.role.code in ['super_admin']:
                queryset = self.model.objects.all()
            elif self.request.user.role.code in ['admin']:
                queryset = self.model.objects.filter(is_active=True)                
            else:
                queryset = self.model.objects.filter(is_active=True)  # not completed yet
        
        if app_label_class_name == 'rbac_permission':
            if self.request.user.role.code in ['super_admin']:
                queryset = self.model.objects.all()
            elif self.request.user.role.code in ['admin']:
                queryset = self.model.objects.filter(is_active=True, feature__is_active=True)
            else:
                queryset = self.model.objects.filter(is_active=True, id__in=self.request.user.role.permission.all())
        
        if app_label_class_name == 'rbac_role':
            if self.request.user.role.code in ['super_admin']:
                queryset = self.model.objects.all()
            elif self.request.user.role.code in ['admin']:
                queryset = self.model.objects.filter(~Q(id=1))  # admin can see all roles except role_id=1 or super_user
            else:
                queryset = self.model.objects.filter(id=self.request.user.role.id)
        
        if app_label_class_name == 'rbac_user':
            if self.request.user.role.code in ['super_admin']:
                queryset = self.model.objects.all()
            if self.request.user.role.code in ['admin']:
                # admin can not see super_admin details
                queryset = self.model.objects.filter(~Q(role_id=1))
            else:
                # Other user  can see only their personal user details
                queryset = self.model.objects.filter(id=self.request.user.id)  
        return queryset
        
        
        
        
        
        
        
        
        
        
        
        