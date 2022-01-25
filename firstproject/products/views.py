from itertools import product
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from products.models import Product
from products.producer import publish
from products.serializers import ProductSerializer
# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    def getAll(self, request): # /api/products
        products=Product.objects.all()
        serializer=ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request): # /api/products
        serializer= ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product-created',serializer.data)
        return Response(serializer.data, status= status.HTTP_201_CREATED)

    def get(self, request, pk=None): # /api/products/<str:id>
        product=Product.objects.get(id=pk)
        serializer=ProductSerializer(product)
        publish('product-returned',serializer.data)
        return Response(serializer.data)

    def update(self, request, pk=None): # /api/products/<str:id>
         product = Product.objects.get(id=pk)
         serializer = ProductSerializer(instance=product, data=request.data)
         serializer.is_valid(raise_exception=True)
         publish('product-updated',serializer.data)
         serializer.save()
         return Response(data= serializer.data, status= status.HTTP_202_ACCEPTED)
        
       
    def delete(self, request, pk=None):
        product = Product.objects.get(id=pk)
        publish('product-deleted',pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
