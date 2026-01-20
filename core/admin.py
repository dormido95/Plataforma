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

@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_price', 'bio_short')
    # ¡Esto permite editar el precio sin entrar al perfil!
    list_editable = ('subscription_price',)

from django.utils.html import format_html

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'creator', 'status_tag')

    def status_tag(self, obj):
        import datetime
        if obj.end_date > datetime.datetime.now():
            return format_html('<b style="color:green;">Activa</b>')
        return format_html('<b style="color:red;">Vencida</b>')
    
    status_tag.short_description = 'Estado'

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
    
    date_hierarchy = 'created_at'

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True