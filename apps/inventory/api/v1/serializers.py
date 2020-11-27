from rest_framework import serializers
from apps.inventory.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not  send to api response


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not send to api response


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not send to api response


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not send to api response


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not send to api response


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not send to api response


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')  # These fields will not send to api response
