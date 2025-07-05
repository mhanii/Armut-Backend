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

@method_decorator(csrf_exempt, name='dispatch')
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
        if len(password) >= 8:
            try:
                if User.objects.filter(username=email).exists():
                    if User.objects.get(username=email).is_active:
                        return Response({'error':'Email already registered'})
                    else:
                        # Directly activate the user if not already active
                        user = User.objects.get(username=email)
                        user.is_active = True
                        user.set_password(password)
                        user.save()
                        return Response({'success':'User activated and password set!'})
                else:
                    user = User.objects.create_user(username=email, password=password, is_active=True)
                    return Response({'success':'User created and activated successfully'})
            except Exception as err:
                return Response({'error':f'Something went wrong:{err}'})
        else:
            return Response({'error':'Password too short (must be at least 8 characters)'})

@method_decorator(csrf_exempt, name='dispatch')
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
                return Response({'success':'User logged in','email':email,})
            else:
                return Response({'error':'Email or password is incorrect'})
        except:
            return Response({'error':'Something went wrong'})

@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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




@method_decorator(csrf_exempt, name='dispatch')
class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        users = User.objects.all()
        users = UserSerializer(users,many=True)

        return Response(users.data)
    

@method_decorator(csrf_exempt, name='dispatch')
class GetUsersProfileView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        userProfiles = userProfile.objects.all()
        userProfiles = userProfileSerializer(userProfiles,many=True)

        return Response(userProfiles.data)
    

@method_decorator(csrf_exempt, name='dispatch')
class GetUsersAddressView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        userAddresses = userAddress.objects.all()
        userAddresses = userAddressSerializer(userAddresses,many=True)

        return Response(userAddresses.data)
    
@method_decorator(csrf_exempt, name='dispatch')
class GetUsersVerificationStateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        userVerification = Verification.objects.all()
        userVerification = userVerificationSerializer(userVerification,many=True)

        return Response(userVerification.data)