from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    # URL for MongoDB ObjectId format (uploaded products)
    # Change this to point to uploaded_product_detail instead of product_detail
    re_path(r'^product/(?P<product_id>[0-9a-fA-F]{24})/?$', views.uploaded_product_detail, name='product_detail'),
    # URL for static products with numeric IDs
    path('product/static/<int:product_id>/', views.static_product_detail, name='static_product_detail'),
    path('sell/', views.sell, name='sell'),
    path('cars/', views.car, name='car'),
    path('bikes/', views.bike, name='bike'),
    path('parts/', views.parts, name='parts'),
    path('contact/', views.contact, name='contact'),
]
