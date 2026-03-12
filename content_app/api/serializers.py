from rest_framework import serializers
from content_app.models import BaseInfo, OfferDetail, Orders, Offers, Reviews


class OfferDetailFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the complete details of an offer, including all fields.
    Primarily used for displaying offer details.
    """
    delivery_time_in_days = serializers.IntegerField(source='delivery_time', allow_null=True, required=False)
    revisions = serializers.IntegerField(source='revision', default=1, required=False)
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]
    
    def to_representation(self, instance):
        """
        Override the default representation to ensure that the delivery_time_in_days field is returned as an integer, even if the original value is a string containing non-numeric characters.
        This method attempts to extract digits from the delivery_time field and convert it to an integer, returning 0 if no valid digits are found or if any exceptions occur during the process.
        """
 
        ret = super().to_representation(instance)
        try:
            val = ret.get('delivery_time_in_days')
            if val is not None:
                digits = "".join(filter(str.isdigit, str(val)))
                ret['delivery_time_in_days'] = int(digits) if digits else 0
        except Exception:
            pass
        return ret


    
class OfferDetailSerializer(serializers.ModelSerializer): #for offerdeails/<id>/
    """
    Serializer for offer details, used for creating and updating offer details.
    This serializer is designed to handle the input for offer details, allowing clients
    to create or update offer details with the necessary fields. It includes validation and transformation of the input data to match the model's requirements.
    """
    revisions = serializers.IntegerField(source='revision')
    delivery_time_in_days = serializers.IntegerField(source='delivery_time', allow_null=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def to_representation(self, instance):
        """
        Override the default representation to ensure that the delivery_time_in_days field is returned as an integer, even if the original value is a string containing non-numeric characters.
        This method attempts to extract digits from the delivery_time field and convert it to an integer, returning 0 if no valid digits are found or if any exceptions occur during the process."""
        ret = super().to_representation(instance)
        try:
            val = ret.get('delivery_time_in_days')
            if val is not None:
                digits = "".join(filter(str.isdigit, str(val)))
                ret['delivery_time_in_days'] = int(digits) if digits else 0
        except Exception:
            pass
        return ret



class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offers model, including nested offer details and user information.
    This serializer is used for both listing and creating offers. It includes nested serialization for offer details and
    user information, as well as custom create and update methods to handle the nested data appropriately.
    """
    details = OfferDetailFullSerializer(many=True)
    min_price = serializers.DecimalField(source='price', max_digits=10, decimal_places=2 , read_only=True)
    min_delivery_time = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

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
        ]

    def to_representation(self, instance):
        """
        Override the default representation to conditionally include or exclude certain fields based on the request method.
        For POST requests, specific fields related to pricing, delivery time, and user details are removed from the response to streamline the data returned after creating an offer.
     """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and request.method == 'POST':
            # When you Post an offer, you don't need all the details about the offer, so we remove some fields to simplify the response
            fields_to_remove = ['min_price', 'min_delivery_time', 'user', 'created_at', 'updated_at']
            for field in fields_to_remove:
                representation.pop(field, None)
        else:
            # For GET requests, only include id and url of offer details
            if 'details' in representation:
                short_details = []
                for detail in instance.details.all():
                    url = f"/api/offerdetails/{detail.id}/"
                    if request:
                        url = request.build_absolute_uri(url)
                    short_details.append({
                        "id": detail.id,
                        "url": url
                    })
                representation['details'] = short_details
                
        return representation

    def create(self, validated_data):
        """
        Custom create method to handle the creation of an offer along with its associated offer details. This method processes the nested offer details data, 
        creates the main offer, and then creates each offer detail while calculating the minimum price and delivery time for the offer.
        """
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
      """
      Custom update method to handle the updating of an offer along with its associated offer details. This method processes the nested offer details data,
      updates the main offer, and then updates or creates each offer detail while recalculating the
      minimum price and delivery time for the offer."""
      details_data = validated_data.pop('details', None)

    # Update Main Offer fields
      for attr, value in validated_data.items():
        setattr(instance, attr, value)
      instance.save()

      if details_data is not None:
        # All existing details delete and new details createn
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
        """
        Method to retrieve the user ID associated with the offer's business.
        This method checks if the offer has an associated business and returns the user ID of that business. If there is no associated business, it returns None.
        """
        return obj.business.id if obj.business else None




class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Orders model, including custom fields for offer details and user information.
    This serializer is used for creating and retrieving orders. It includes custom fields to handle the offer 
    details and user information, as well as a custom create method to handle the creation of orders based on the provided offer details.
    """
    offer_detail_id = serializers.IntegerField(write_only=True)
    customer_user = serializers.SerializerMethodField(read_only=True)
    business_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Orders
        fields = [
            'id', 
            'offer_detail_id', 
            'customer_user', 
            'business_user', 
            'title', 
            'revisions', 
            'delivery_time_in_days', 
            'price', 
            'features', 
            'offer_type', 
            'status', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    def get_customer_user(self, obj):
        return obj.customer_user.user.id if obj.customer_user and obj.customer_user.user else None

    def get_business_user(self, obj):
        return obj.business_user.user.id if obj.business_user and obj.business_user.user else None

    def create(self, validated_data):
        """
        Custom create method to handle the creation of an order based on the provided offer details. This method retrieves the offer details using the provided offer_detail_id,
        determines the customer and business users, calculates the delivery time in days, and creates a new order with the relevant information from the offer details."""
        offer_detail_id = validated_data.pop('offer_detail_id')
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError({"offer_detail_id": "Offer detail not found."})

        request = self.context.get('request')
        if request and hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False):
            customer_user = getattr(request.user, 'userprofile', None)
        else:
            customer_user = None

        business_user = offer_detail.offer.business
        
        delivery_days = 0
        if offer_detail.delivery_time:
            digits = "".join(filter(str.isdigit, str(offer_detail.delivery_time)))
            if digits:
                delivery_days = int(digits)

        order = Orders.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revision,
            delivery_time_in_days=delivery_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress',
        )
        return order


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reviews model, including custom fields for reviewer information.
    This serializer is used for creating and retrieving reviews. It includes a custom field to handle the reviewer information,
    as well as a custom create method to handle the creation of reviews based on the authenticated user.
    """
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Reviews
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        extra_kwargs = {
            'business_user': {'required': True, 'allow_null': False},
            'rating': {'required': True},
            'description': {'required': True, 'allow_blank': False}
        }

    def validate(self, data):
        """
        Custom validation to ensure that only customers can post reviews and that users cannot review themselves. This method checks the authenticated user's profile to determine if they are a customer and ensures that they are not attempting to review their own business.
        If the user is not a customer or if they are trying to review themselves, a validation
        error is raised with an appropriate message."""
        request = self.context.get('request')
        if request and request.method == 'POST':
            user_profile = getattr(request.user, 'userprofile', None)
            
            # Check if user is a customer
            if not user_profile or user_profile.type != 'customer':
                raise serializers.ValidationError({"detail": "Only customers are allowed to post a review."})
            
            # Additional check: You cannot review yourself because your are the business user
            business_user = data.get('business_user')
            if business_user == user_profile:
                raise serializers.ValidationError({"detail": "You cannot review yourself."})
                
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['reviewer'] = getattr(request.user, 'userprofile', None)
        return super().create(validated_data)


class BaseInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the BaseInfo model, used to represent aggregated information about reviews, business profiles, and offers.
    This serializer is used for retrieving aggregated data such as the total number of reviews, average rating
    """
    class Meta:
        model = BaseInfo
        fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']

