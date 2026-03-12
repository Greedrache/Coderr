from django.db import models

# OFFERS
class Offers(models.Model):
    business = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    min_delivery_time = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Offers"

    def __str__(self):
        return self.title
    
    
class OfferDetail(models.Model):
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ]
    
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=200)
    revision = models.IntegerField(default=1)
    delivery_time = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type.capitalize()} (Revision {self.revision})"






# ORDERS
class Orders(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    customer_user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='customer_orders', null=True)
    business_user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='business_orders', null=True)
  #  offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders', null=True)
    title = models.CharField(max_length=200, blank=True)
    revisions = models.IntegerField(default=1)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(blank=True, null=True)
    offer_type = models.CharField(max_length=20, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} for {self.title}"


class Reviews(models.Model):
    reviewer = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='given_reviews', null=True)
    business_user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='received_reviews', null=True)
    rating = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.reviewer} for {self.business_user}: {self.rating} stars"




class BaseInfo(models.Model):
    review_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    business_profile_count = models.IntegerField(default=0)
    offer_count = models.IntegerField(default=0)

    def __str__(self):
        return f"BaseInfo: {self.review_count} reviews, {self.average_rating} average rating, {self.business_profile_count} business profiles, {self.offer_count} offers"