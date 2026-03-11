from django.urls import path
from .views import OffersView, OfferDetailView, OrderView, OrderDetailView, OrderCountView, CompletedOrderCountView, ReviewsView, ReviewDetailView, BaseInfoView, OfferDetailDetailView

urlpatterns = [
    path('offers/', OffersView.as_view(), name='offer-list'), # This endpoint is for listing and creating offers, so it uses the OffersView which is a ListCreateAPIView.
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailDetailView.as_view(), name='offer-detail-detail'),

    path('orders/', OrderView.as_view(), name='order-list'), # This endpoint is for creating new orders, so it uses the OrderView which is a CreateAPIView.
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count'),

    path('reviews/', ReviewsView.as_view(), name='review-list'), # This endpoint is for listing and creating reviews, so it uses the ReviewsView which is a ListCreateAPIView.
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    
    path('base-info/', BaseInfoView.as_view(), name='base-info'),    
]