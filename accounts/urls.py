from django.urls import path
from .views import SignupView,GetCSRFToken,CheckAuthenticatedView,LoginView,LogoutView,DeleteAccountView,GetUsersView,GetUsersProfileView,GetUsersAddressView,VerifyView,GetUsersVerificationStateView


urlpatterns = [
    path('authenticated',CheckAuthenticatedView.as_view()),
    path('csrf_cookie',GetCSRFToken.as_view()),
    path('signup',SignupView.as_view()),
    path('login',LoginView.as_view()),
    path('logout',LogoutView.as_view()),
    path('delete',DeleteAccountView.as_view()),
    path('get_users',GetUsersView.as_view()),
    path("get_profiles",GetUsersProfileView.as_view()),
    path("get_address",GetUsersAddressView.as_view()),
    path("verify",VerifyView.as_view()),
    path("get_verifications",GetUsersVerificationStateView.as_view()),
]