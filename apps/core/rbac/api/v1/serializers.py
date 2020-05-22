from rest_framework import serializers
from apps.core.rbac.models import *
        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
    def validate_schema_name(self, value):
        """ Check that schema_name is in lower case. """
        if value not in value.lower():
            raise serializers.ValidationError("Schema Name must be in lower case")
        return value
        
        
class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
        
        
class TenantSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Domain
        fields = '__all__'
        
    def create(self, validated_data):
        """ Create and return a new Tenant. """     
        customer = Customer.objects.create(**validated_data.get('customer'))
        domain = Domain()
        domain.domain = validated_data.get('domain')
        domain.sub_domain = validated_data.get('sub_domain')
        domain.tenant = customer
        domain.customer = customer
        domain.is_active = validated_data.get('is_active')
        domain.save()
        return domain
        
        
class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        """ Create and return a new User. """
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
        
    def update(self, instance, validated_data):
        """ Update and return an existing User instance. """        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.position = validated_data.get('position', instance.position)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
