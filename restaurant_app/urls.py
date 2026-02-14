from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path("add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("clear-cart/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-complete/", views.order_complete, name="order_complete"),
    path("cart/set/<int:item_id>/", views.set_cart_qty, name="set_cart_qty"),
    path("send-feedback/", views.send_feedback, name="send_feedback"),




]
