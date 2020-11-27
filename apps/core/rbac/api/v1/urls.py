from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .viewsets import *


router = routers.DefaultRouter()
router.register('client', ClientViewSet) #done
router.register('domain', DomainViewSet) #done
router.register('tenant', TenantViewSet) #done
router.register('feature', FeatureViewSet) #done
router.register('sidebar', SidebarViewSet) #done
router.register('permission', PermissionViewSet) #done
router.register('role', RoleViewSet) #done
router.register('group', GroupViewSet) #done
router.register('user', UserViewSet) #done
router.register('branch', BranchViewSet)
router.register('department', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('login/', login, name='rbac_login'),
    path('logout/', logout, name='rbac_logout'),    
    path('registration/', registration, name='rbac_registration'),
    path('username-existence/', check_username_existence, name='rbac_username_existance'), #done
    path('email-existence/', check_email_existence, name='rbac_email_existance'), #done
    path('active/<str:activation_url>/', active_user, name='rbac_active'), #done
    path('reset-password-send-url/', reset_password_send_url, name='rbac_reset_password_send_url'),  #done
    path('reset-password/<str:activation_url>/', reset_password, name='rbac_reset_password'),  #done
    path('user-info/', get_user_info, name='rbac_user_info'), #done
]
