import secrets
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

from apps.core.base.utils.basic import random_hex_code


def get_activation_url():
    return secrets.token_hex(nbytes=16)


class AuditTrail(models.Model):
    hashed_id = models.CharField(null=True, blank=True, max_length=8, unique=True)
    created_by = models.CharField(max_length=500, blank=True, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set added_by during the first save.
            self.created_by = exposed_request.user.id  # exposed_request comes from RequestExposerMiddleware
            self.updated_by = self.created_by
            # For each object a new unique hashed id will be generated.
            # This will be used instead of default id of each model.
            self.hashed_id = random_hex_code()
        else:
            self.updated_by = exposed_request.user.id
        super(AuditTrail, self).save(*args, **kwargs)


class ActivityLog(AuditTrail):
    store_json = models.TextField(blank=True)
    description = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=50)
    browser_details = models.CharField(max_length=500)

    def __str__(self):
        return self.description


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
    order_for_sidebar = models.FloatField(default=1111)
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
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )

    middle_name = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False,
                                validators=[RegexValidator(
                                    regex='[-a-zA-Z0-9_.]{4,50}$',
                                    message='Username contains alphanumeric, underscore and period(.). Length: 4 to 50'
                                )])
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, null=False, blank=False, related_name='user_role', default=1)
    mobile_number = models.CharField(max_length=12)
    gender = models.IntegerField(choices=GENDER, default=1)
    address = models.TextField(blank=True, null=True)
    country = models.IntegerField()
    activation_url = models.CharField(max_length=500, blank=False, default=get_activation_url)
    profile_picture = models.ImageField(upload_to='user/profile_picture/', blank=True, null=True)
    signature = models.ImageField(upload_to='user/signature/', blank=True, null=True)

    initial = models.BooleanField(null=False, blank=False, default=True)
    need_to_change_password = models.BooleanField(null=False, blank=False, default=False)
    password_updated_at = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(null=False, blank=False, default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    unsuccessful_attempt = models.IntegerField(null=False, blank=False, default=0)

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
    is_active = models.BooleanField(default=True)
    user = models.ManyToManyField(User, blank=True, related_name='group_users')


class UserPassword(AuditTrail):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    hash = models.CharField(null=False, blank=False, max_length=200)


class Branch(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Branch contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    customer = models.ForeignKey(Customer, related_name='branch_customer', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True, related_name='branch_users')
    group = models.ManyToManyField(Group, blank=True, related_name='branch_groups')
    address = models.TextField(blank=True)

    def get_users(self):
        # this will return all users id from user and group field
        user_id = self.user.values_list('id', flat=True)
        all_user = [(user_id + g.user.values_list('id', flat=True)) for g in self.group]
        return list(dict.fromkeys(all_user[0]))  # all unique user list

    def __str__(self):
        return self.name

class Department(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Department contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    branch = models.ForeignKey(Branch, related_name='department_branch', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True, related_name='department_users')
    group = models.ManyToManyField(Group, blank=True, related_name='department_groups')

    def get_users(self):
        # this will return all users id from user and group field
        user_id = self.user.values_list('id', flat=True)
        all_user = [(user_id + g.user.values_list('id', flat=True)) for g in self.group]
        return list(dict.fromkeys(all_user[0]))  # all unique user list

    def __str__(self):
        return self.name









