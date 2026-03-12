from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from content_app.api.permissions import IsOwnerOrReadOnly
from content_app.api.serializers import OfferSerializer, OrderSerializer, ReviewSerializer, BaseInfoSerializer, OfferDetailSerializer
from content_app.models import OfferDetail, BaseInfo
from content_app.models import Offers, Orders, Reviews
from users_app.models import UserProfile
from rest_framework.views import APIView, Response


#OffersSection
class OffersView(generics.ListCreateAPIView):
    """
    View for listing and creating offers. This view allows users to retrieve a list of all offers and create new offers.
    The list of offers is ordered by creation date in descending order. When creating a new offer, the business field is automatically set to the authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Offers.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.userprofile)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific offer. This view allows users to retrieve the details of a specific offer,
    update the offer if they are the owner, and delete the offer if they are the owner.
    """
    queryset = Offers.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class OfferDetailDetailView(generics.RetrieveAPIView):
    """
    View for retrieving the details of a specific offer detail. This view allows users to retrieve the details of a specific offer detail.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer



#OrderSection
class OrderView(generics.CreateAPIView):
    """
    View for creating a new order. This view allows users to create a new order based on the provided offer details.
    The offer details are validated and used to create a new order. The customer user is set to the authenticated user's profile, and the business user is set based on the offer details.
    """
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific order. This view allows users to retrieve the details of a specific order,
    update the order if they are the customer or business user, and delete the order if they are the customer or business user.
    """
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


class OrderCountView(generics.RetrieveAPIView):
    """
    View for retrieving the count of in-progress orders for a specific business user. This view allows users to retrieve the number of orders that are currently in progress for a given business user.
    The business user is identified by the provided user ID, and the count is calculated based on the orders associated with that business user that have a status of 'in_progress'."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs['pk']
        if not User.objects.filter(userprofile__id=business_user_id).exists():
            return Response({"detail": "User not found."}, status=404)
            
        order_count = Orders.objects.filter(business_user_id=business_user_id, status='in_progress').count()
        return Response({'order_count': order_count})


class CompletedOrderCountView(generics.RetrieveAPIView):
    """
    View for retrieving the count of completed orders for a specific business user. This view allows users to retrieve the number of orders that have been completed for a given business user.
    The business user is identified by the provided user ID, and the count is calculated based on the orders associated with that business user that have a status of 'completed'.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs['pk']
        if not User.objects.filter(userprofile__id=business_user_id).exists():
            return Response({"detail": "User not found."}, status=404)
            
        completed_order_count = Orders.objects.filter(business_user_id=business_user_id, status='completed').count()
        return Response({'completed_order_count': completed_order_count})



#ReviewSection
class ReviewsView(generics.ListCreateAPIView):
    """
    View for listing and creating reviews. This view allows users to retrieve a list of all reviews and create new reviews.
    The list of reviews can be filtered by business user or reviewer, and ordered by update date or rating.
    """
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific review. This view allows users to retrieve the details of a specific review,
    update the review if they are the reviewer, and delete the review if they are the reviewer.
    """
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer


#BaseInfoSection
class BaseInfoView(APIView):
    """
    View for retrieving aggregated information about reviews, business profiles, and offers. This view allows users to 
    retrieve the total number of reviews, average rating, total number of business profiles, and total number of offers.
    The information is aggregated from the Reviews, UserProfile, and Offers models and returned in a single response.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        review_count = Reviews.objects.count()
        
        avg_rating = Reviews.objects.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(avg_rating, 1) if avg_rating is not None else 0.0
        
        # Taking 'type' or similar field logic into account for business profiles
        business_profile_count = UserProfile.objects.filter(type='business').count()
        offer_count = Offers.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        })