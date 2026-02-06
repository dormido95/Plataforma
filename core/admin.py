import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import CreatorProfile, Content, Subscription

# --- CONFIGURACIÓN GLOBAL ---
admin.site.site_header = "Plataforma Pro Admin"
admin.site.index_title = "Gestión de Creadores"

# --- FUNCIONES Y FILTROS EXTRA ---

class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Rango de Precio'
    parameter_name = 'price_range'
    def lookups(self, request, model_admin):
        return [('low', 'Económico (<10)'), ('mid', 'Medio (10-50)'), ('high', 'Premium (>50)')]
    def queryset(self, request, queryset):
        if self.value() == 'low': return queryset.filter(subscription_price__lt=10)
        if self.value() == 'mid': return queryset.filter(subscription_price__gte=10, subscription_price__lte=50)
        if self.value() == 'high': return queryset.filter(subscription_price__gt=50)

@admin.action(description='Promoción: Precio a 1 USD')
def set_promo_price(modeladmin, request, queryset):
    queryset.update(subscription_price=1.00)

# --- INLINES ---
class ContentInline(admin.TabularInline):
    model = Content
    extra = 0
    readonly_fields = ('created_at',)

# --- MODELOS ---

@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_price', 'total_fans', 'bio_short')
    
    # 1. hacer click en el precio para entrar al perfil también
    list_display_links = ('user', 'subscription_price')
    
    list_editable = () # Lo quitamos de editable para que el link funcione mejor
    list_filter = (PriceRangeFilter,)
    
    # 2. Ayuda para el administrador
    search_fields = ('user__username', 'user__email')
    search_help_text = "Busca creadores por nombre de usuario o correo electrónico."
    
    empty_value_display = "- No asignado -"
    inlines = [ContentInline]
    actions = [set_promo_price]

    fieldsets = (
        ('Datos de Usuario', {'fields': ('user',)}),
        ('Configuración Monetaria', {'fields': ('subscription_price',)}),
        ('Información Pública', {
            'classes': ('collapse',),
            'fields': ('bio',),
        }),
    )

    def bio_short(self, obj):
        return obj.bio[:50] + "..." if obj.bio else None
    bio_short.short_description = 'Resumen de Bio'

    def total_fans(self, obj):
        return obj.subscription_set.count()
    total_fans.short_description = 'Fans'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
    list_filter = ('creator', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    save_on_top = True
    save_as = True
    search_fields = ('title', 'description')
    
    # 3. Ayuda visual en la búsqueda de contenido
    search_help_text = "Filtra por título del post o palabras en la descripción."


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'creator', 'status_tag', 'end_date')
    list_select_related = ('subscriber', 'creator__user')
    raw_id_fields = ('subscriber', 'creator')
    list_per_page = 25
    list_filter = ('end_date', 'creator')
    search_fields = ('subscriber__username', 'creator__user__username')
    
    # 4. Evita scroll infinito al buscar
    show_full_result_count = False 

    def status_tag(self, obj):
        if obj.end_date > datetime.date.today():
            return format_html('<b style="color:green;">Activa</b>')
        return format_html('<b style="color:red;">Vencida</b>')
    status_tag.short_description = 'Estado'