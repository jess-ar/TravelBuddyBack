from django.urls import path
from .views import RegisterView, LoginView, UserListView, DeleteUserView, search_images, LogoutView, UserMeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('delete_user/<str:username>/', DeleteUserView.as_view(), name='delete_user'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('images/search/', search_images, name='search_images'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserMeView.as_view(), name='user-me'),

    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
