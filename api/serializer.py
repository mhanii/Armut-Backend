from rest_framework import serializers
from .views import Product, Banner
from .models import Store, ProductImage, Color, Category
from django.db import models


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class ProductImageSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    class Meta:
        model = ProductImage
        fields = ['id', 'imageUrl', 'color']


class ProductTypeSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'imageUrl']


class ProductImageCreateSerializer(serializers.ModelSerializer):
    color = serializers.CharField(required=False)  # Accept color name or ID as string
    
    class Meta:
        model = ProductImage
        fields = ['imageUrl', 'color']
    
    def create(self, validated_data):
        color_data = validated_data.pop('color', None)
        if color_data:
            # Try to find color by name first, then by ID
            try:
                color = Color.objects.get(name__iexact=color_data)
            except Color.DoesNotExist:
                try:
                    color = Color.objects.get(id=color_data)
                except (Color.DoesNotExist, ValueError):
                    color = None
            validated_data['color'] = color
        return super().create(validated_data)


class ColorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['name', 'hex_code']


class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(required=False, write_only=True)
    image_colors = serializers.ListField(required=False, write_only=True)
    customization_options = serializers.JSONField(required=False, write_only=True)
    delivery_options = serializers.JSONField(required=False, write_only=True)
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'discount', 'customization_options', 'delivery_options', 'images', 'image_colors']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        image_colors_data = validated_data.pop('image_colors', [])
        customization_options = validated_data.pop('customization_options', {})
        delivery_options = validated_data.pop('delivery_options', {})
        
        # Create the product
        product = Product.objects.create(**validated_data)
        
        # Create or get colors from customization_options
        color_objects = []
        if customization_options and 'colors' in customization_options:
            for color_data in customization_options['colors']:
                color_name = color_data['name'].lower()
                hex_code = color_data['hex']
                
                # Try to find existing color by name (case-insensitive) or hex_code
                existing_color = Color.objects.filter(
                    models.Q(name__iexact=color_name) | models.Q(hex_code=hex_code)
                ).first()
                
                if existing_color:
                    color_objects.append(existing_color)
                else:
                    # Create new color
                    new_color = Color.objects.create(
                        name=color_name,
                        hex_code=hex_code
                    )
                    color_objects.append(new_color)
        
        # Add colors to product
        if color_objects:
            product.colors.set(color_objects)
        
        # Create images with color assignments
        for i, image_file in enumerate(images_data):
            color_name = image_colors_data[i] if i < len(image_colors_data) else None
            color_obj = None
            
            if color_name:
                # Use filter().first() to avoid MultipleObjectsReturned
                color_obj = Color.objects.filter(name__iexact=color_name).first()
            
            ProductImage.objects.create(
                product=product,
                imageUrl=image_file,
                color=color_obj
            )
        
        return product
    
    def to_representation(self, instance):
        # Include colors in response
        data = super().to_representation(instance)
        data['colors'] = ColorSerializer(instance.colors.all(), many=True).data
        return data

