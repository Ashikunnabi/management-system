from rest_framework.permissions import BasePermission


class UserAccessApiBasePermission(BasePermission):
    def __init__(self, model):
        self.model = model
        super(UserAccessApiBasePermission, self).__init__()

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:            
            return self.has_object_permission(request, view, self.model)

    def has_object_permission(self, request, view, obj):
        if request.user.role.id == 1:
            # super_admin can do all action
            permissions = [_ for i in request.user.role.permission.all().values_list('code') for _ in i]
        else:
            # others can do active options
            permissions = [_ for i in request.user.role.permission.filter(is_active=True).values_list('code') for _ in i]
        app_label = str(obj._meta.app_label)
        object_class_name = str(obj._meta.model_name)
        app_label_class_name = app_label+ '_' + object_class_name
        has_operation_permissions = [_.split('.')[0] for _ in permissions if app_label_class_name in _]

        methods = {
            'view': ['GET'], # remove this kind of permission
            'detail_view': ['GET'],
            'self_view': ['GET'],
            'list_view': ['GET'],
            'add': ['POST'],
            'change': ['PUT', 'PATCH'],
            'delete': ['DELETE'],
        }
        for _ in has_operation_permissions:
            if request.method in methods[_]:
                return True
        return False

        
        
        
        
        
        
        