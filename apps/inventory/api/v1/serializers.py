from rest_framework import serializers
from apps.inventory.models import *

# These fields will not send to api response
exclude_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = exclude_fields


class JsTreeCategorySerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        exclude = exclude_fields

    def get_text(self, obj):
        return obj.name

    def get_children(self, obj):
        return True if obj.parent is not None else False

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = exclude_fields


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        exclude = exclude_fields


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = exclude_fields


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = exclude_fields


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        exclude = exclude_fields


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        exclude = exclude_fields


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        exclude = exclude_fields
