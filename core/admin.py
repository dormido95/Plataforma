import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import CreatorProfile, Content, Subscription

# --- CONFIGURACIÓN DE INTERFAZ ---
admin.site.site_header = "Plataforma Pro Admin"
admin.site.index_title = "Gestión de Creadores y Suscripciones"

# --- FUNCIONES EXTRA ---

# Filtro personalizado para el precio
class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Rango de Precio'
    parameter_name = 'price_range'
    def lookups(self, request, model_admin):
        return [('low', 'Barato (<10)'), ('mid', 'Medio (10-50)'), ('high', 'Premium (>50)')]
    def queryset(self, request, queryset):
        if self.value() == 'low': return queryset.filter(subscription_price__lt=10)
        if self.value() == 'mid': return queryset.filter(subscription_price__gte=10, subscription_price__lte=50)
        if self.value() == 'high': return queryset.filter(subscription_price__gt=50)

@admin.action(description='Promoción: Precio a 1 USD')
def set_promo_price(modeladmin, request, queryset):
    queryset.update(subscription_price=1.00)

# --- CLASES ADMIN ---

class ContentInline(admin.TabularInline): 
    model = Content
    extra = 0 # Para que no aparezcan filas vacías por defecto
    readonly_fields = ('created_at',)

@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    # ¿Qué columnas queremos ver en la tabla principal?
    list_display = ('user', 'subscription_price', 'total_fans', 'bio_short')
    
    # editar el precio sin entrar al perfil
    list_editable = ('subscription_price',)
    
    # Filtros y búsquedas
    list_filter = (PriceRangeFilter,)
    search_fields = ('user__username', 'user__email')
    
    # Configuración de interfaz
    inlines = [ContentInline]
    actions = [set_promo_price]
    empty_value_display = "- No asignado -"

    # Organización por secciones
    fieldsets = (
        ('Datos de Usuario', {'fields': ('user',)}),
        ('Configuración de Perfil', {'fields': ('subscription_price',)}),
        ('Biografía y Detalles', {'classes': ('collapse',), 'fields': ('bio',)}),
    )

    # Crearr "columnas inventadas"
    def bio_short(self, obj):
        return obj.bio[:50] + "..." if obj.bio else None
    bio_short.short_description = 'Resumen de Bio'

    def total_fans(self, obj):
        return obj.subscription_set.count()
    total_fans.short_description = 'Total Fans'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'creator', 'status_tag', 'end_date')
    
    # Carga los datos de usuario de un solo viaje a la DB
    list_select_related = ('subscriber', 'creator__user')
    
    # Paginación y búsqueda
    list_per_page = 25
    search_fields = ('subscriber__username', 'creator__user__username')
    list_filter = ('end_date',)

    def status_tag(self, obj):
        if obj.end_date > datetime.date.today():
            return format_html('<b style="color:green;">Activa</b>')
        return format_html('<b style="color:red;">Vencida</b>')
    status_tag.short_description = 'Estado'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
    
    # Filtros y navegación
    list_filter = ('creator', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'description')
    
    # Comportamiento del formulario
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    save_on_top = True
    save_as = True