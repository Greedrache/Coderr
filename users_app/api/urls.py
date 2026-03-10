from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, CustomLoginView, BusinessProfileList, CustomerProfileList
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profile/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('profiles/business/', BusinessProfileList.as_view(), name='userprofile-business'),
    path('profiles/customer/', CustomerProfileList.as_view(), name='userprofile-customer'),

    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Endpoint for obtaining auth token
]