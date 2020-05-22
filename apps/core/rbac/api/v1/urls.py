from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .viewsets import *


router = routers.DefaultRouter()
router.register('customer', CustomerViewSet) #done
router.register('domain', DomainViewSet) #done
router.register('tenant', TenantViewSet) #done
router.register('feature', FeatureViewSet) #done
router.register('permission', PermissionViewSet) #done
router.register('role', RoleViewSet) #done
router.register('user', UserViewSet) #done

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('registration/', registration, name='account_registration'),
    path('username-existence/', check_username_existence, name='account_username_existance'), #done
    path('email-existence/', check_email_existence, name='account_email_existance'), #done
    path('active/<str:activation_url>/', active_user, name='account_active'), #done
    path('reset-password-send-url/', reset_password_send_url, name='account_reset_password_send_url'),  #done
    path('reset-password/<str:activation_url>/', reset_password, name='account_reset_password'),  #done
    path('user-info/', get_user_info, name='account_user_info'), #done
]
