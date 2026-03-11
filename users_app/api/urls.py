from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, CustomLoginView, BusinessProfileList, CustomerProfileList
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'), # This endpoint is for listing and creating user profiles, so it uses the UserProfileList view which is a ListCreateAPIView.
    path('profile/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('profiles/business/', BusinessProfileList.as_view(), name='userprofile-business'),
    path('profiles/customer/', CustomerProfileList.as_view(), name='userprofile-customer'),

    path('registration/', RegistrationView.as_view(), name='registration'), # This endpoint is for user registration, so it uses the RegistrationView which is a custom view that handles user registration logic.
    path('login/', CustomLoginView.as_view(), name='login'),  # This endpoint is for user login, so it uses the CustomLoginView which is a custom view that handles user authentication and token generation.
]