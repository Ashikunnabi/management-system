import secrets
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

    
class AuditTrail(models.Model):
    created_by = models.CharField(max_length=500, blank=True)
    updated_by = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set added_by during the first save.
            self.created_by = exposed_request.user.id  # exposed_request comes from RequestExposerMiddleware
            self.updated_by = self.created_by
        else:
            self.updated_by = exposed_request.user.id
        super(AuditTrail, self).save(*args, **kwargs)
    


def get_activation_url():
    return secrets.token_hex(nbytes=16)
    
    
class Customer(TenantMixin):
    STATUS = (
        (1, 'General User'),
        (2, 'Pro User'),
    )
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    logo = models.FileField(upload_to='customer/', blank=True, null=True)
    address = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.name
    

class Domain(DomainMixin):
    sub_domain = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(
                                regex='[a-z]{4,100}$',
                                message='Sub domain contains lower case alphabets only. Length: 4 to 100'
                            )]
                            )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=False, related_name='domain_customer')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class Feature(AuditTrail):
    title = models.CharField(max_length=50, blank=False, null=False, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=False, null=False, unique=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    parent = models.CharField(max_length=5, blank=True, null=True)
    customers = models.ManyToManyField(Customer, blank=True, related_name='feature_customers')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
        

class Permission(AuditTrail):
    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)
    code = models.CharField(max_length=50, blank=False, unique=True)
    is_active = models.BooleanField(default=True)    
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=False, blank=False, related_name='permission_feature')

    def __str__(self):
        return self.name


class Role(AuditTrail):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    code = models.CharField(max_length=50, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    permission = models.ManyToManyField(Permission, related_name='role_permissions')

    def __str__(self):
        return self.name
    
    
class User(AbstractUser):
    position = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=50,
                                unique=True,
                                null=False,
                                blank=False,
                                validators=[RegexValidator(
                                    regex='[-a-zA-Z0-9_.]{4,50}$',
                                    message='Username contains alphanumeric, underscore and period(.). Length: 4 to 50'
                                )])
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, null=False, blank=False, related_name='user_role', default=1)
    activation_url = models.CharField(max_length=500, blank=False, default=get_activation_url)
    has_to_change_password = models.BooleanField(default=True)
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
        


class Group(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Group contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    status = models.BooleanField(default=True)
    user = models.ManyToManyField(User, blank=True, related_name='group_users')
    
    
    
    
    
    
    
    
    
