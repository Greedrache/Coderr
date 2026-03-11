from rest_framework import serializers
from content_app.models import BaseInfo, OfferDetail, Orders, Offers, Reviews


class OfferDetailFullSerializer(serializers.ModelSerializer):
    delivery_time_in_days = serializers.CharField(source='delivery_time', allow_blank=True, allow_null=True, required=False)
    revisions = serializers.IntegerField(source='revision', default=1, required=False)
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]


    
class OfferDetailSerializer(serializers.ModelSerializer): #for offerdeails/<id>/
    revisions = serializers.IntegerField(source='revision')
    delivery_time_in_days = serializers.CharField(source='delivery_time', allow_null=True, allow_blank=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']



class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailFullSerializer(many=True)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(source='price', max_digits=10, decimal_places=2 , read_only=True)
    min_delivery_time = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Offers
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and request.method == 'POST':
            fields_to_remove = ['min_price', 'min_delivery_time', 'user_details', 'user']
            for field in fields_to_remove:
                representation.pop(field, None)
                
        return representation

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        
        request = self.context.get('request') if hasattr(self, 'context') else None
        if request and hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False):
            business_profile = getattr(request.user, 'userprofile', None)
            if business_profile:
                validated_data['business'] = business_profile

        offer = Offers.objects.create(**validated_data)

        prices = []
        delivery_times = []

        for detail in details_data:
            price = detail.get('price')
            delivery = detail.get('delivery_time') 
            revision = detail.get('revision', 1)

            if price:
                prices.append(price)
            if delivery:
                delivery_times.append(delivery)

            OfferDetail.objects.create(
                offer=offer,
                title=detail['title'],
                revision=revision,
                price=price,
                delivery_time=delivery,
                features=detail.get('features', []),
                offer_type=detail['offer_type']
            )

        if prices:
            offer.price = min(prices)
        if delivery_times:
            offer.min_delivery_time = min(delivery_times)
        offer.save()

        return offer

    def update(self, instance, validated_data):
      details_data = validated_data.pop('details', None)

    # Update Hauptfelder
      for attr, value in validated_data.items():
        setattr(instance, attr, value)
      instance.save()

      if details_data is not None:
        # Alte Details löschen (oder optional nur anpassen)
        instance.details.all().delete()
        for detail in details_data:
            OfferDetail.objects.create(
                offer=instance,
                title=detail['title'],
                revision=detail.get('revisions', 1),
                price=detail.get('price'),
                delivery_time=detail.get('delivery_time_in_days'),
                features=detail.get('features', []),
                offer_type=detail['offer_type']
            )

      return instance

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

