from rest_framework import serializers
from users_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']




class BusinessProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business profiles. This serializer is used to retrieve a list of business profiles with their basic information.
    It includes fields such as username, first name, last name, file, location, telephone number, description, working hours, type, email, and creation date.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer profiles. This serializer is used to retrieve a list of customer profiles with their basic information.
    It includes fields such as username, first name, last name, file, location, telephone number, description, working hours, type, email, and creation date.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']





class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration. This serializer is used to handle the registration of new users, including validation of
    email uniqueness, password confirmation, and user type. It includes fields for username, email, password, repeated password, and type.
    The save method creates a new user and associated user profile based on the provided data, and sets the appropriate permissions for admin users.
    """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.CharField(required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('repeated_password'):
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data
    
    def validate_type(self, value):
        if value not in ['customer', 'admin', 'business']:
            raise serializers.ValidationError("Type must be either 'customer', 'admin', or 'business'.")
        return value

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        type = self.validated_data.get('type', 'customer')
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        profile = user.userprofile
        profile.type = type.lower()
        profile.save()

    
        if type.lower() == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user
    

