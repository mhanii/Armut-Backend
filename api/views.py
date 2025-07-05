from django.shortcuts import render, get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchQuery , SearchVector, SearchRank
from django.urls import reverse_lazy
from django.core import serializers
from django.db.models import Q
from .models import Product, Banner,Category, Store, ProductImage
from .serializer import ProductTypeSerializer, BannerSerializer, StoreSerializer, ProductImageSerializer, CategorySerializer, ProductCreateSerializer
from django.http import FileResponse,JsonResponse,HttpResponse,HttpRequest
from django.views.generic.edit import CreateView
from rest_framework  import permissions
from django.db.models.functions import Lower
from django.db.models import CharField
CharField.register_lookup(Lower)
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProductTypeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if category:
            category_names = [c.strip() for c in category.split(',')]
            queryset = queryset.filter(category__name__in=[c.lower() for c in category_names])
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

class BannerView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class DiscountView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.exclude(discount = 0).order_by("-discount")
    serializer_class = ProductTypeSerializer


def ServeImage(request,image_file,folder):
    
    file = open("/static/images/"+folder+"/"+ image_file ,'rb')
    print(file)
    return FileResponse(file)


class ProductDetails(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self,request,link):
        product = Product.objects.get(link=link)
        serializer = ProductTypeSerializer(product)
        return Response(serializer.data)


class SearchView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self,request):
        q = request.GET.get("q",'')
        
        vector = SearchVector('name','description')
        query = SearchQuery(q)
        queryset = Product.objects.annotate(rank=SearchRank(vector,query)).filter(rank__gte=0.001).order_by("-rank")  
        serializer = ProductTypeSerializer(queryset,many=True)

        print(query)
           
        return Response(serializer.data)

class CategoryView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self,request,cate):
        categoryText = Category.objects.get(name__lower=cate)
        print(categoryText)
        querysets = Product.objects.filter(category=categoryText.id)
        serializer = ProductTypeSerializer(querysets,many=True)
        return Response(serializer.data)
    
class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Only allow vendors to edit/delete their own store
        return Store.objects.filter(owner=self.request.user)

class VendorProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        # Only products for the vendor's store(s)
        return Product.objects.filter(store__owner=self.request.user)
    def perform_create(self, serializer):
        store_id = self.request.data.get('store')
        store = Store.objects.get(id=store_id, owner=self.request.user)
        serializer.save(store=store)

class VendorProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a product by its id (if owned by vendor)
    PUT/PATCH: Update a product by its id (if owned by vendor)
    DELETE: Delete a product by its id (if owned by vendor)
    """
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Product.objects.filter(store__owner=self.request.user)
    def get_object(self):
        obj = super().get_object()
        if obj.store.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not have permission to access this product.')
        return obj

class AdminStoreListView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    # Optionally, restrict to admin users only
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Not authorized.'}, status=403)
        return super().get(request, *args, **kwargs)

class AdminProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Not authorized.'}, status=403)
        return super().get(request, *args, **kwargs)

class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)
        if product.store.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not have permission to add images to this product.')
        serializer.save(product=product)

class ProductImageDeleteView(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        obj = super().get_object()
        if obj.product.store.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not have permission to delete images from this product.')
        return obj

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class StoreListView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.AllowAny]

class ProductByVendorView(generics.RetrieveAPIView):
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.AllowAny]
    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        product_id = self.kwargs['product_id']
        return get_object_or_404(Product, id=product_id, store__owner__id=vendor_id)

class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.AllowAny]

class VendorProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    @transaction.atomic
    def perform_create(self, serializer):
        # Ensure user is a vendor
        if not hasattr(self.request.user, 'userprofile') or self.request.user.userprofile.user_type != 'vendor':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only vendors can create products.')
        
        # Get the user's store automatically
        try:
            store = Store.objects.get(owner=self.request.user)
        except Store.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('You must have a store to create products.')
        
        # Create the product with the store
        product = serializer.save(store=store)
        return product

# Health check endpoint
class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            "status": "healthy",
            "message": "Armut API is running successfully"
        }, status=status.HTTP_200_OK)
    
