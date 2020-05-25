from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.register, name='register'),
	# path('<int:delete_id>/delete/', views.delete, name='delete'),
	# path('<int:user_id>/deactivate/', views.deactivate, name='deactivate'),
	# path('<int:update_id>/update/', views.update, name='update'),
]
