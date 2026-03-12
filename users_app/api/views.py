from rest_framework import generics
from users_app.models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer, BusinessProfileListSerializer, CustomerProfileListSerializer
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework import permissions


class UserProfileList(generics.ListCreateAPIView):
    """
    View for listing and creating user profiles. This view allows users to retrieve a list of all user profiles and create new user profiles.
    The list of user profiles is ordered by creation date in descending order. When creating a new user profile, the user field is automatically set to the authenticated user's ID.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific user profile. This view allows users to retrieve the details of a specific user profile,
    update the user profile if they are the owner, and delete the user profile if they are the owner.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsProfileOwnerOrReadOnly()]
        return [permissions.IsAuthenticated()]
    

class CustomLoginView(ObtainAuthToken):
    """
    View for user login. This view allows users to log in by providing their username and password. The view validates
    the credentials and returns an authentication token if the credentials are valid. If the credentials are invalid, it returns an error response.   
    """
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_obj = User.objects.get(username=username)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        serializer = self.serializer_class(data={'username': username, 'password': password}, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)  
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    """
    View for user registration. This view allows users to register by providing their username, email, password, repeated password, and user type.
    The view validates the provided data, creates a new user and associated user profile, and returns an authentication token if the registration is successful. 
    If the registration fails due to validation errors, it returns an error response with the details of the validation errors.
    """
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class BusinessProfileList(generics.ListAPIView):
    """
    View for listing business profiles. This view allows users to retrieve a list of all business profiles.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = BusinessProfileListSerializer
    pagination_class = None

class CustomerProfileList(generics.ListAPIView):
    """
    View for listing customer profiles. This view allows users to retrieve a list of all customer profiles.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = CustomerProfileListSerializer
    pagination_class = None