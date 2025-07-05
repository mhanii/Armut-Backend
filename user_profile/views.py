from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Product
from rest_framework import status
from .models import User,userProfile,userAddress, Order, OrderItem
from .serializers import UserProfileInfoSerializer,UserProfileAddressSerializer, OrderSerializer
import json
from cart.models import userCart, userCartItem
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class GetUserProfileView(APIView):
    def get(self,request):
        user                        = request.user
        email                       = user.email
        try:
            user                        = User.objects.get(id=user.id)
            user_profile                = userProfile.objects.get(user=user)

            user_profile                = UserProfileInfoSerializer(user_profile)


            return Response({'profile':user_profile.data,"email":email})
        except:
            return Response({"error":"Something went wrong! "})


class UpdateWholeUserProfileView(APIView):
    def put(self,request):
        try:
            user                    = request.user
            email                   = user.email

            data                    = request.data
            first_name              = data['first_name']
            last_name               = data['last_name']
            phone_number            = data['phone_number']
            town                    = data['town']
            area                    = data['area']
            road                    = data['road']
            building                = data['building']
            floor                   = data['floor']
            door_number             = data['door_number']
            address_1               = data['address_1']

            user                    = User.objects.get(id = user.id)


            userProfile.objects.filter(user = user.id).update(first_name=first_name,last_name=last_name,phone_number=phone_number)
            userAddress.objects.filter(user = user.id).update(town=town,area=area,road=road,building=building,floor=floor,door_number=door_number,address_1=address_1)
            user_profile            = userProfile.objects.get(user=user.id)
            user_profile            = UserProfileInfoSerializer(user_profile)
        except Exception as er:
            return Response({'error':f'Something went wrong: {er}'})


        return Response({'profile':user_profile.data,"email":email})
    





class UpdateUserProfilePersonalInfoView(APIView):
    def put(self,request):
        try:
            user                    = request.user
            email                   = user.email

            data                    = request.data
            first_name              = data['first_name']
            last_name               = data['last_name']
            phone_number            = data['phone_number']
            # new_email               = data['email']

            user                    = User.objects.get(id = user.id)


            userProfile.objects.filter(user = user.id).update(first_name=first_name,last_name=last_name,phone_number=phone_number)
            user_profile            = userProfile.objects.get(user =user.id)
            user_profile            = UserProfileInfoSerializer(user_profile)
        except Exception as er:
            return Response({'error':f'Something went wrong: {er}'})


        return Response({'profile':user_profile.data,"email":email})
    


class GetUserProfileAddresses(APIView):
    def get(self,request):
        user = request.user
        id = user.id
        try:
            addresses   = userAddress.objects.filter(user = id).order_by('title')
            addresses   = UserProfileAddressSerializer(addresses,many=True,)
            addresses = json.dumps(addresses.data)

            return Response(json.loads(addresses))
        except Exception as err:
            return Response({f"error:{err}"})
        
@method_decorator(csrf_exempt, name='dispatch')
class AddUserProfileAddressView(APIView):
    def post(self,request):
        data                    = self.request.data
        user                    = request.user
        user                    = User.objects.get(id = user.id)
        try:
            title                   = data['title']
            town                    = data['town']
            area                    = data['area']
            road                    = data['road']
            building                = data['building']
            floor                   = data['floor']
            door_number             = data['door_number']
            address_1               = data['address_1']
            address = userAddress(user= user,title=title,town=town,area=area,road=road,building = building,floor=floor,door_number=door_number,address_1=address_1)
            address.save()


            return Response({"success"})
        except Exception as err:
            return Response({f"error:{err}"})


class DeleteUserProfileAddressView(APIView):
    def delete(self,request,format=None):
        data            = request.data
        user            = request.user
        try:
            addressID             = data["id"]
            addressRequested    = userAddress.objects.get(id=addressID,user=user.id).delete()
            return Response({"success":"Address deleted successfully! "})
        except Exception as err:
            return Response({"error":f"Something went wrong!:{err}"})
            





class UpdateUserProfileAddressView(APIView):
    def put(self,request):
        try:
            user                    = request.user
            email                   = user.email
            data                    = request.data
            id                      = data['id']
            title                   = data['title']
            town                    = data['town']
            area                    = data['area']
            road                    = data['road']
            building                = data['building']
            floor                   = data['floor']
            door_number             = data['door_number']
            address_1               = data['address_1']

            user                    = User.objects.get(id = user.id)


            userAddress.objects.filter(user = user.id).filter(id=id).update(title=title,town=town,area=area,road=road,building=building,floor=floor,door_number=door_number,address_1=address_1)
            user_address            = userAddress.objects.get(user=user.id)
            user_address            = UserProfileAddressSerializer(user_address)
        except Exception as er:
            return Response({'error':f'Something went wrong: {er}'})


        return Response({'address':user_address.data,"email":email})
    

class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class CreateOrderFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        user = request.user
        try:
            cart = userCart.objects.get(user=user)
            cart_items = cart.items.all()
            if not cart_items:
                return Response({'error': 'Cart is empty.'}, status=400)
            shipping_address_id = request.data.get('shipping_address')
            if not shipping_address_id:
                return Response({'error': 'Shipping address required.'}, status=400)
            total = 0
            for item in cart_items:
                total += item.quantity * item.item.price
            order = Order.objects.create(user=user, total=total, shipping_address_id=shipping_address_id)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.item,
                    quantity=item.quantity,
                    price=item.item.price
                )
            cart.items.clear()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=201)
        except userCart.DoesNotExist:
            return Response({'error': 'Cart does not exist.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class VendorOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Only allow vendors
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'vendor':
            return Response({'error': 'Not authorized.'}, status=403)
        order_items = OrderItem.objects.filter(product__store__owner=request.user)
        order_ids = order_items.values_list('order_id', flat=True).distinct()
        orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    