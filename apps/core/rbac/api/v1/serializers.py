from rest_framework import serializers

from apps.core.rbac.models import *

# These fields will not  send to api response
exclude_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')


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
        datatables_always_serialize = ('id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Create and return a new User. """
        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
            position=validated_data.get('position'),
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            role=validated_data.get('role'),
            mobile_number=validated_data.get('mobile_number'),
            gender=validated_data.get('gender'),
            address=validated_data.get('address'),
            is_active=int(self.context['request'].data.get('account_status', 0)),
            country=validated_data.get('country'),
        )
        if self.context['request'].data.get('file_profile_picture') is not None:
            user.profile_picture = self.context['request'].data['file_profile_picture']
        if self.context['request'].data.get('file_signature') is not None:
            user.signature = self.context['request'].data['file_signature']
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        """ Update and return an existing User instance. """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.position = validated_data.get('position', instance.position)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)
        instance.is_active = int(self.context['request'].data.get('account_status', instance.is_active))
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        if self.context['request'].data.get('file_profile_picture') is not None:
            if self.context['request'].data.get('file_profile_picture') == 'null':
                instance.profile_picture = None
            else:
                instance.profile_picture = self.context['request'].data['file_profile_picture']
        if self.context['request'].data.get('file_signature') is not None:
            if self.context['request'].data.get('file_signature') == 'null':
                instance.signature = None
            else:
                instance.signature = self.context['request'].data['file_signature']
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    # As parent is already a field that's why we named 'parent_human_readable' and tell the source field name
    parent_human_readable = serializers.StringRelatedField(source='parent')
    parent_hashed_id = serializers.SerializerMethodField()
    group_hashed_id = serializers.SerializerMethodField()
    branch_tree_view = serializers.SerializerMethodField()
    is_active_parent = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        exclude = exclude_fields

    def get_parent_hashed_id(self, obj):
        if obj.parent:
            return str(obj.parent.hashed_id)
        return None

    def get_group_hashed_id(self, obj):
        if obj.group:
            groups = obj.group.all()
            return [group.hashed_id for group in groups]
        return None

    def get_branch_tree_view(self, obj):
        path = obj.name
        if obj.parent:
            def parent(branch):
                nonlocal path
                path = branch.name + "/" + path
                if branch.parent:
                    parent(branch.parent)
                else:
                    return path

            parent(obj.parent)
        return path

    def get_is_active_parent(self, obj):
        """
        If any parent(immediate or grand parent)'s is_active value of the obj/branch is false then the parent.is_active
         of the obj/branch's value will be false. As if the parent is not active then user can't edit the child
         branches...
        :param obj: is a single branch object
        :return: a boolean value
        """
        is_active_parent_branch = True
        if obj.parent:
            def parent(parent_branch):
                nonlocal is_active_parent_branch
                if not parent_branch.is_active:
                    is_active_parent_branch = False
                if parent_branch.parent:
                    is_active_parent_branch = parent(parent_branch.parent)
                return is_active_parent_branch
            is_active_parent_branch = parent(obj.parent)
        return is_active_parent_branch

    def get_fields(self):
        """add this method to add 'subbranches' field"""
        fields = super(BranchSerializer, self).get_fields()
        fields['subbranches'] = BranchSerializer(many=True, read_only=True, allow_null=True)
        return fields


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = exclude_fields

