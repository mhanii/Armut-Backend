from django.urls import path
from .views import ProductView,ServeImage,BannerView,DiscountView,ProductDetails,SearchView,CategoryView,StoreListCreateView,StoreDetailView,VendorProductListCreateView,VendorProductDetailView,AdminStoreListView,AdminProductListView,CategoryListView,StoreListView,ProductByVendorView,ProductRetrieveView,VendorProductCreateView,HealthCheckView

urlpatterns = [
        path('health/', HealthCheckView.as_view(), name='health-check'),
        path('products/', ProductView.as_view(), name='product-list'),
        path('products/<int:pk>/', ProductRetrieveView.as_view(), name='product-detail'),
        path('static/images/<str:folder>/<str:image_file>',ServeImage,name="serve_image"),
        path('banners',BannerView.as_view(),name='banner-list'),
        path('discount',DiscountView.as_view(),name='discount-list'),
        path('product/<slug:link>/',ProductDetails.as_view(),name='server_details'),
        path('search/',SearchView.as_view(),name='search'),
        path('category/<slug:cate>/',CategoryView.as_view(),name='category'),
        path('stores/', StoreListCreateView.as_view(), name='store-list-create'),
        path('stores/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
        path('vendor/products/', VendorProductListCreateView.as_view(), name='vendor-product-list-create'),
        path('vendor/products/create/', VendorProductCreateView.as_view(), name='vendor-product-create'),
        path('vendor/products/<int:pk>/', VendorProductDetailView.as_view(), name='vendor-product-detail'),
        path('admin/stores/', AdminStoreListView.as_view(), name='admin-store-list'),
        path('admin/products/', AdminProductListView.as_view(), name='admin-product-list'),
        path('categories/', CategoryListView.as_view(), name='category-list'),
        path('stores/all/', StoreListView.as_view(), name='store-list'),
        path('stores/<int:vendor_id>/products/<int:product_id>/', ProductByVendorView.as_view(), name='product-by-vendor'),
]