from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('product/<str:product_slug>.<str:product_id>', views.product, name="product"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('update_variation/', views.updateVariation, name="update_variation"),
	path('process_order/', views.processOrder, name="process_order"),
]
