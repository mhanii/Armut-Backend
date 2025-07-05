from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework  import permissions
from .serializers import UserSerializer,userProfileSerializer,userAddressSerializer,userVerificationSerializer
from user_profile.models import userProfile,userAddress
from user_profile.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie , csrf_protect
from django.utils.decorators import method_decorator
from .utils import generate_verification_code,send_verification_email
from .models import Verification
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import Store

@method_decorator(csrf_protect,name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self,request,format=None):
        user = request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                return Response({'isAuthenticated':'success'})
            else:
                return Response({'isAuthenticated':'error'})
        except:
            return Response({'error':'Something went wrong'})
        



@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request,format=None):
        data = self.request.data

        email = data['email']
        password = data['password']
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        user_type = data.get('user_type', 'customer')
        if len(password) >= 8:
            try:
                if User.objects.filter(username=email).exists():
                    user = User.objects.get(username=email)
                    if user.is_active:
                        return Response({'error':'Email already registered'})
                    else:
                        # Directly activate the user if not already active
                        user.is_active = True
                        user.set_password(password)
                        user.save()
                        # Update or create userProfile
                        profile, created = userProfile.objects.get_or_create(user=user)
                        profile.first_name = first_name
                        profile.last_name = last_name
                        profile.user_type = user_type
                        profile.save()
                        
                        # If user is a vendor and doesn't have a store, create one
                        if user_type == 'vendor' and not Store.objects.filter(owner=user).exists():
                            store_name = f"{first_name}'s Store" if first_name else f"{email}'s Store"
                            Store.objects.create(
                                name=store_name,
                                description=f"Welcome to {store_name}",
                                owner=user
                            )
                        
                        return Response({'success':'User activated and profile updated!'})
                else:
                    user = User.objects.create_user(username=email, password=password, is_active=True)
                    # Create userProfile with provided info
                    userProfile.objects.create(user=user, first_name=first_name, last_name=last_name, user_type=user_type)
                    
                    # If user is a vendor, create a default store
                    if user_type == 'vendor':
                        store_name = f"{first_name}'s Store" if first_name else f"{email}'s Store"
                        Store.objects.create(
                            name=store_name,
                            description=f"Welcome to {store_name}",
                            owner=user
                        )
                    
                    return Response({'success':'User created, activated, and profile set successfully'})
            except Exception as err:
                return Response({'error':f'Something went wrong:{err}'})
        else:
            return Response({'error':'Password too short (must be at least 8 characters)'})

@method_decorator(csrf_protect,name='dispatch')
class VerifyView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self,request):
        try:
            data            = request.data
            code            = data["code"]
            email           = data["email"]  
            user            = User.objects.get(username=email)
            verification = get_object_or_404(Verification, user=user.id)

            if code == verification.code:
                verification.is_verified = True
                verification.save()
                user.is_active = True
                user.save()


                user_profile, created = userProfile.objects.get_or_create(
                    user=user,
                    defaults={'first_name': '', 'last_name': '', 'phone_number': ''}
                )

                user_profile.save()


                return Response({"success":"Account activated! "})
            else:
                # Handle invalid code scenario
                return Response({"error":"Verification code is not correct! "})
        except Exception as e:
            return Response({"error":f"Something went wrong! : {e} "})

    

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request,format=None):
        data = self.request.data

        try:
            email = data['email']
            password = data['password']



            user  = auth.authenticate(username=email,password= password)

            if user is not None:
                auth.login(request,user)
                # Get user profile data
                try:
                    profile = userProfile.objects.get(user=user)
                    profile_data = userProfileSerializer(profile).data
                except userProfile.DoesNotExist:
                    profile_data = {}
                response = {'success': 'User logged in', 'email': email}
                response.update(profile_data)
                return Response(response)
            else:
                return Response({'error':'Email or password is incorrect'})
        except:
            return Response({'error':'Something went wrong'})

class LogoutView(APIView):
    def post(self,request,format=None):
        try:
            auth.logout(request)
            return Response({'success':'Logged out'})
        except:
            return Response({'error':'Something went wrong'})


@method_decorator(ensure_csrf_cookie,name='dispatch')    
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request,format=None):
        return Response({'success':'CSRF cookie set'})


class DeleteAccountView(APIView):
    def delete(self,request,format=None):

        try:
            user = request.user
            print(user)
            User.objects.get(id = user.id).delete()

            return Response({'sucess','User deleted'})
        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong'})




class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        users = User.objects.all()
        users = UserSerializer(users,many=True)

        return Response(users.data)
    

class GetUsersProfileView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        userProfiles = userProfile.objects.all()
        userProfiles = userProfileSerializer(userProfiles,many=True)

        return Response(userProfiles.data)
    

class GetUsersAddressView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        userAddresses = userAddress.objects.all()
        userAddresses = userAddressSerializer(userAddresses,many=True)

        return Response(userAddresses.data)
    
class GetUsersVerificationStateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        userVerification = Verification.objects.all()
        userVerification = userVerificationSerializer(userVerification,many=True)

        return Response(userVerification.data)