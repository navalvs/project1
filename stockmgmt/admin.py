from django.contrib import admin
from .forms import StockCreateForm
from .models import Stock

# Register your models here.

from .models import *

class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'quantity']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']

admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)



# Define the custom admin action
def clear_history(modeladmin, request, queryset):
    queryset.delete()
clear_history.short_description = "Clear selected history"

# Register the custom action for the StockHistory model
@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    actions = [clear_history]




