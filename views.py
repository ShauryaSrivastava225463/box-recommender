from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Box


def home(request):
    """Render the interactive HTML demo page."""
    return render(request, 'shipping/home.html')
from .serializers import ProductSerializer, BoxSerializer, RecommendBoxRequestSerializer
from .services import find_best_box


class ProductListCreateView(APIView):
    """
    GET  /api/products/   — list all products
    POST /api/products/   — create a new product
    """

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoxListCreateView(APIView):
    """
    GET  /api/boxes/   — list all boxes
    POST /api/boxes/   — create a new box
    """

    def get(self, request):
        boxes = Box.objects.all()
        serializer = BoxSerializer(boxes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendBoxView(APIView):
    """
    POST /api/recommend/
    Body: { "product_id": <int> }

    Returns the cheapest box that fits the given product.
    """

    def post(self, request):
        req_serializer = RecommendBoxRequestSerializer(data=request.data)
        if not req_serializer.is_valid():
            return Response(req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = req_serializer.validated_data['product_id']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": f"Product with id {product_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        best_box = find_best_box(product)

        if best_box:
            message = f"Box '{best_box.name}' is recommended for product '{product.name}'."
        else:
            message = f"No suitable box found for product '{product.name}'. Consider adding a larger box."

        return Response({
            "product": ProductSerializer(product).data,
            "recommended_box": BoxSerializer(best_box).data if best_box else None,
            "message": message,
        })
