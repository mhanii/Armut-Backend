from django.urls import path
from .views import GetUserProfileView,UpdateWholeUserProfileView,UpdateUserProfileAddressView,\
UpdateUserProfilePersonalInfoView,AddUserProfileAddressView,GetUserProfileAddresses,DeleteUserProfileAddressView,\
UserOrderListView, CreateOrderFromCartView, VendorOrderListView
urlpatterns= [
    path('user',GetUserProfileView.as_view()),
    path('setprofile',UpdateWholeUserProfileView.as_view()),
    path("setpersonalinfo",UpdateUserProfilePersonalInfoView.as_view()),
    path("updateaddress",UpdateUserProfileAddressView.as_view()),
    path("addaddress",AddUserProfileAddressView.as_view()),
    path("deleteaddress",DeleteUserProfileAddressView.as_view()),
    path("getaddresses",GetUserProfileAddresses.as_view()),
    path('orders', UserOrderListView.as_view(), name='user-orders'),
    path('orders/create', CreateOrderFromCartView.as_view(), name='create-order-from-cart'),
    path('vendor/orders', VendorOrderListView.as_view(), name='vendor-orders'),
]