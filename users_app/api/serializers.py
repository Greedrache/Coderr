from rest_framework import serializers
from users_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.Serializer):
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
        if value not in ['regular', 'admin', 'buisness']:
            raise serializers.ValidationError("Type must be either 'regular', 'admin', or 'buisness'.")
        return value

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        type = self.validated_data.get('type', 'regular')
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        if type == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user