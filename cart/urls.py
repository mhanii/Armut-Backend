from django.urls import path
from .views import SetCart,AddToCart,RemoveFromCart,ViewCart,ClearCart,DecreaseCartItemQuantity,LoadCart

urlpatterns= [
    path("setcart",SetCart.as_view()),
    path("addtocart",AddToCart.as_view()),
    path("removefromcart",RemoveFromCart.as_view()),
    path("loadcart",LoadCart.as_view()),
    path("clearcart",ClearCart.as_view()),
    path("decrease_quantity", DecreaseCartItemQuantity.as_view(),name='decrease-cart-item-quantity'),

]