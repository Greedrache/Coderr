from rest_framework import serializers
from content_app.models import BaseInfo, Orders, Offers, Reviews



class OrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    business_id = serializers.IntegerField()
    offer_id = serializers.IntegerField()

class OfferSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class ReviewSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    business_id = serializers.IntegerField()
    rating = serializers.IntegerField()
    comment = serializers.CharField(allow_blank=True)



class BaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInfo
        fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']

