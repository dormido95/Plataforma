from django.contrib import admin
from .models import CreatorProfile, Content, Subscription

admin.site.register(CreatorProfile)
admin.site.register(Content)
admin.site.register(Subscription)


@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
 
    list_display = ('user', 'subscription_price', 'bio_short')
    
  
    def bio_short(self, obj):
        return obj.bio[:50] + "..." 
    bio_short.short_description = 'Resumen de Bio'

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'creator', 'end_date')
    

    search_fields = ('subscriber__username', 'creator__user__username')
    

    list_filter = ('end_date',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
  
    readonly_fields = ('created_at',)



class ContentInline(admin.TabularInline):
    model = Content
    extra = 1  

@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_price')
    
    inlines = [ContentInline]