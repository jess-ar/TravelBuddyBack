from django.urls import path
from .views import RegisterView, LoginView, UserListView, DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('delete/<str:username>/', DeleteUserView.as_view(), name='delete-user'),  # Asegúrate de que esta ruta esté presente
]
