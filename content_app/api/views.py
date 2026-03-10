from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from content_app.api.serializers import OfferSerializer, OrderSerializer, ReviewSerializer, BaseInfoSerializer
from content_app.models import Offers, Orders
from rest_framework.views import APIView, Response


#OffersSection
class OffersView(generics.ListCreateAPIView):
    queryset = Offers.objects.all()
    serializer_class = OfferSerializer


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offers.objects.all()
    serializer_class = OfferSerializer



#OrderSection
class OrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()


class OrderDetailView(generics.RetrieveAPIView):
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
    queryset = Orders.objects.all()
    serializer_class = BaseInfoSerializer