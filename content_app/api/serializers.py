from rest_framework import serializers
from content_app.models import BaseInfo, OfferDetail, Orders, Offers, Reviews


class OfferDetailFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revision", "delivery_time", "price", "features", "offer_type"]



class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailFullSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(source='price', max_digits=10, decimal_places=2 , read_only=True)
    min_delivery_time = serializers.CharField( max_length=100, allow_blank=True, allow_null=True, required=False)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Offers
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_user(self, obj):
      return obj.business.id if obj.business else None
    
    def get_user_details(self, obj):
     if obj.business:
        return {
            "first_name": obj.business.first_name or "",
            "last_name": obj.business.last_name or "",
            "username": obj.business.username or "NotAvailable",
        }
     return {}





class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['user_id', 'business_id', 'offer_id']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['user_id', 'business_id', 'rating', 'comment']


class BaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInfo
        fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']

