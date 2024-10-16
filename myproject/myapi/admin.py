from django.contrib import admin
from .models import Item

# Register your models here.


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at', 'name')
    search_fields = ('name', )


