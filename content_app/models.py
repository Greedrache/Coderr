from django.db import models

# Create your models here.

class Orders(models.Model):
    user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE)
    business = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='business_orders')
    offer = models.ForeignKey('offers_app.Offer', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user} for {self.offer} at {self.order_date}"


class Offers(models.Model):
    business = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reviews(models.Model):
    user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE)
    business = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE, related_name='business_reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.business}: {self.rating} stars"




class BaseInfo(models.Model):
    review_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    business_profile_count = models.IntegerField(default=0)
    offer_count = models.IntegerField(default=0)

    def __str__(self):
        return f"BaseInfo: {self.review_count} reviews, {self.average_rating} average rating, {self.business_profile_count} business profiles, {self.offer_count} offers"