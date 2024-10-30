from django.contrib import admin
from .models import SoilType

# Register your models here.


@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name',
                    'water_retention_capacity', 'permeability_rate')
    search_fields = ('type_name',)
    list_filter = ('water_retention_capacity',)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('type_name')
