from django.urls import path, include
from shop import views

# app_name = 'shop'

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('products/<int:myid>', views.prodview, name="Products"),
    path('checkout/', views.checkout, name="Checkout"),
    path('cart/', views.cart, name="Cart"),
    path('register/', views.register, name="Register"),
    path('user_login/', views.user_login, name="User_Login"),
    path('handlerequest/', views.handlerequest, name="HandleRequest")

]
