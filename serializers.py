from rest_framework import serializers
from .models import Product, Box


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'length', 'width', 'height', 'weight']


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'name', 'inner_length', 'inner_width', 'inner_height', 'max_weight', 'cost']


class RecommendBoxRequestSerializer(serializers.Serializer):
    """Input: just the product id."""
    product_id = serializers.IntegerField()


class RecommendBoxResponseSerializer(serializers.Serializer):
    """Output: recommended box details (or a 'no box found' message)."""
    product = ProductSerializer()
    recommended_box = BoxSerializer(allow_null=True)
    message = serializers.CharField()
