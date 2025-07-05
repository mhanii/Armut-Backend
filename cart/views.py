from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Product
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User,userCart,userCartItem
from .serializers import UserCartSerializer
from api.serializer import ProductTypeSerializer
import json
# Create your views here.

class ViewCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        try:
            cart = userCart.objects.get(user=user)
            cart = UserCartSerializer(cart)
            return Response({"data":cart.data})
        except userCart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)
        except Exception as err:
            return Response({"error":f"Something went wrong! {err}"}, status=500)



class LoadCart(APIView):
    permission_classes = []  # Temporarily remove authentication requirement
    
    def get(self, request):
        user = request.user
        
        # Debug information
        if not user.is_authenticated:
            return Response({
                "error": "User not authenticated",
                "user_type": str(type(user)),
                "session_id": request.session.session_key,
                "cartItems": [],
                "amount": 0
            })

        try:
            user_cart = userCart.objects.get(user=user)
            cart_items = user_cart.items.all()

            # Build the response data with cart item details
            cart_data = []
            for cart_item in cart_items:
                item = Product.objects.get(id=cart_item.item.id)
                item = ProductTypeSerializer(item)
                item_data = {
                    "id": cart_item.item.id,
                    "name": cart_item.item.name,
                    "product": item.data,
                    "quantity": cart_item.quantity,
                }
                cart_data.append(item_data)

            return Response({"cartItems":cart_data,"amount":len(cart_items)})
        except userCart.DoesNotExist:
            return Response({"cartItems": [], "amount": 0})
        
@method_decorator(csrf_exempt, name='dispatch')
class ClearCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        try:
            cart = userCart.objects.get(user=user)
            cart.items.clear()  # Remove all items from the cart
            return Response("Cart cleared successfully", status=status.HTTP_200_OK)
        except userCart.DoesNotExist:
            return Response("Cart does not exist", status=status.HTTP_404_NOT_FOUND)        
class SetCart(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        items = data.get("cart_items", [])  # Use get() method with a default value to handle missing key gracefully

        # Retrieve the user's cart or create a new one if it doesn't exist
        user_cart, created = userCart.objects.get_or_create(user=user)

        for item_data in items:
            item_id = item_data.get("id")
            amount = item_data.get("amount")

            if item_id and amount:
                product = Product.objects.get(id=item_id)
                cart_item, created = userCartItem.objects.get_or_create(
                    cart=cart_item, item=product, defaults={"quantity": amount}
                )
                if not created:
                    # If the cart item already exists, update its quantity
                    cart_item.quantity = amount
                    cart_item.save()

                user_cart.items.add(cart_item)

        return Response("Cart items added successfully.")

@method_decorator(csrf_exempt, name='dispatch')
class AddToCart(APIView):
    def post(self, request):
        print(request)
        user = request.user
        data = request.data
        item_id = data.get("item_id")
        quantity = data.get("quantity", 1)  # Default quantity to 1 if not provided

        if item_id:
            try:
                product = Product.objects.get(id=item_id)

                # Retrieve the user's cart or create a new one if it doesn't exist
                user_cart, created = userCart.objects.get_or_create(user=user)

                # Check if the item already exists in the cart
                cart_item, created = userCartItem.objects.get_or_create(
                    cart=user_cart, item=product, defaults={"quantity": quantity}
                )
                if not created:
                    # If the item already exists, update its quantity
                    cart_item.quantity += quantity
                    cart_item.save()

                user_cart.items.add(cart_item)

                return Response("Item added to cart successfully.")
            except Product.DoesNotExist:
                return Response("Invalid item ID.", status=400)
        else:
            return Response("Item ID is required.", status=400)

@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCart(APIView):
    def delete(self, request):
        user = request.user
        data = request.data
        item_id = data.get("item_id")

        if item_id:
            try:
                product = Product.objects.get(id=item_id)

                # Retrieve the user's cart and remove the item if it exists
                user_cart = userCart.objects.get(user=user)
                user_cart.items.filter(item=product).delete()

                return Response("Item removed from cart successfully.")
            except Product.DoesNotExist:
                return Response("Invalid item ID.", status=400)
            except userCart.DoesNotExist:
                return Response("Cart does not exist for the user.", status=400)
        else:
            return Response("Item ID is required.", status=400)
        


@method_decorator(csrf_exempt, name='dispatch')
class DecreaseCartItemQuantity(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        item_id = data.get("item_id")

        try:
            cart = userCart.objects.get(user=user)
            print(cart,item_id)
            item = userCartItem.objects.get(cart=cart, item_id=item_id)

            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

            return Response("Item quantity decreased successfully", status=status.HTTP_200_OK)
        except (userCart.DoesNotExist, userCartItem.DoesNotExist):
            return Response("Item or cart does not exist", status=status.HTTP_404_NOT_FOUND)