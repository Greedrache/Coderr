from django.contrib import admin
from .models import Offers, OfferDetail, Orders, Reviews, BaseInfo

# Register your models here.
admin.site.register(Offers)
admin.site.register(OfferDetail)
admin.site.register(Orders)
admin.site.register(Reviews)
admin.site.register(BaseInfo)
