from django.contrib import admin
from .models import CreatorProfile, Content, Subscription

admin.site.register(CreatorProfile)
admin.site.register(Content)
admin.site.register(Subscription)