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
    queryset = Offers.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.userprofile)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offers.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class OfferDetailDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer



#OrderSection
class OrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


class OrderCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs['pk']
        if not User.objects.filter(userprofile__id=business_user_id).exists():
            return Response({"detail": "User not found."}, status=404)
            
        order_count = Orders.objects.filter(business_user_id=business_user_id, status='in_progress').count()
        return Response({'order_count': order_count})


class CompletedOrderCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs['pk']
        if not User.objects.filter(userprofile__id=business_user_id).exists():
            return Response({"detail": "User not found."}, status=404)
            
        completed_order_count = Orders.objects.filter(business_user_id=business_user_id, status='completed').count()
        return Response({'completed_order_count': completed_order_count})



#ReviewSection
class ReviewsView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer


#BaseInfoSection
class BaseInfoView(APIView):
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