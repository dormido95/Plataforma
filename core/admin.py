import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import CreatorProfile, Content, Subscription

# --- CONFIGURACIÓN GLOBAL ---
admin.site.site_header = "Plataforma Pro Admin"
admin.site.index_title = "Gestión de Creadores"

# --- INLINES ---
class ContentInline(admin.TabularInline):
    model = Content
    extra = 0  # No crea filas vacías por defecto
    readonly_fields = ('created_at',)

# --- MODELOS ---

@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    # Columnas, edición rápida y el resumen de bio
    list_display = ('user', 'subscription_price', 'bio_short')
    list_editable = ('subscription_price',)
    search_fields = ('user__username', 'user__email')
    empty_value_display = "- No asignado -"
    
    # Inlines para ver el contenido del creador
    inlines = [ContentInline]

    def bio_short(self, obj):
        if obj.bio:
            return obj.bio[:50] + "..."
        return None
    bio_short.short_description = 'Resumen de Bio'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    # fechas, orden y botones de guardado
    list_display = ('title', 'creator', 'created_at')
    list_filter = ('creator', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    save_on_top = True
    save_as = True
    search_fields = ('title', 'description')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    # semáforo de colores, paginación y filtros
    list_display = ('subscriber', 'creator', 'status_tag', 'end_date')
    list_per_page = 25
    list_filter = ('end_date', 'creator')
    search_fields = ('subscriber__username', 'creator__user__username')

    def status_tag(self, obj):
        # El semáforo de colores 
        if obj.end_date > datetime.date.today():
            return format_html('<b style="color:green;">Activa</b>')
        return format_html('<b style="color:red;">Vencida</b>')
    
    status_tag.short_description = 'Estado'
   