from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .models import CustomUser
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission
from django.conf import settings
from django.http import JsonResponse
import requests
from django.shortcuts import render
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            print("Checking if the serializer data is valid...")

            if serializer.is_valid():
                user = serializer.save()
                print("User saved successfully")

                email = request.data.get('email')
                password = request.data.get('password')
                user = authenticate(username=email, password=password)

                if user is not None:
                    login(request, user)
                    print("User authenticated successfully")

                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)
                    print("Tokens generated successfully")

                    return Response({
                        'access': access_token,
                        'refresh': refresh_token,
                        'message': 'User registered successfully'
                    }, status=status.HTTP_201_CREATED)
                else:
                    print("Authentication failed")
                    return Response({'error': 'Authentication failed.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(f"Validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Unknown error: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            user.delete()
            return Response({'detail': 'User successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


def search_images(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'No query parameter provided'}, status=400)

    headers = {"Ocp-Apim-Subscription-Key": settings.BING_API_KEY}
    params = {"q": query, "count": 10, "license": "public", "imageType": "photo"}
    response = requests.get("https://api.bing.microsoft.com/v7.0/images/search", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        images = [{'url': img['contentUrl'], 'name': img.get('name', '')} for img in data.get('value', [])]
        return JsonResponse(images, safe=False)
    else:
        return JsonResponse({'error': 'Error fetching images from Bing API'}, status=response.status_code)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "avatar": user.profile.avatar.url if user.profile.avatar else None,
        })
