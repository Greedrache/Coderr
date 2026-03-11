from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from content_app.api.permissions import IsOwnerOrReadOnly
from content_app.api.serializers import OfferSerializer, OrderSerializer, ReviewSerializer, BaseInfoSerializer, OfferDetailSerializer
from content_app.models import OfferDetail, BaseInfo
from content_app.models import Offers, Orders
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
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        business_id = self.kwargs['pk']
        order_count = Orders.objects.filter(business_id=business_id).count()
        return Response({'order_count': order_count})


class CompletedOrderCountView(generics.RetrieveAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        business_id = self.kwargs['pk']
        completed_order_count = Orders.objects.filter(business_id=business_id, status='completed').count()
        return Response({'completed_order_count': completed_order_count})



#ReviewSection
class ReviewsView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = ReviewSerializer


#BaseInfoSection
class BaseInfoView(generics.RetrieveAPIView):
    queryset = BaseInfo.objects.all()
    serializer_class = BaseInfoSerializer