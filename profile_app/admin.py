from django.contrib import admin
from .models import Item, UserInventory

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'slot', 'icon')
    search_fields = ('name', 'slug')

@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'is_equipped')
    list_filter = ('user', 'item__slot')
