from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/', views.product, name='product'),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    # Add to Cart
    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path('cart/', views.cart, name='cart'),

    path(
    'cart/update/<int:item_id>/',
    views.update_cart_quantity,
    name='update_cart_quantity'
),

path(
    'cart/remove/<int:item_id>/',
    views.remove_from_cart,
    name='remove_from_cart'
),

path('checkout/', views.checkout, name='checkout'),

path('signup/', views.signup, name='signup'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),

path('place-order/', views.place_order, name='place_order'),

path(
    'order-confirmation/<int:order_id>/',
    views.order_confirmation,
    name='order_confirmation'
),

path('my-orders/', views.my_orders, name='my_orders'),
path('profile/', views.profile, name='profile'),

path(
    'order-detail/<int:order_id>/',
    views.order_detail,
    name='order_detail'
),

path('sale/', views.sale, name='sale'),

path('contact/', views.contact, name='contact'),
]