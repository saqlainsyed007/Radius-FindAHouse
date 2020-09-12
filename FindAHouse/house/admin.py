from django.contrib import admin

from house.models import House

# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    model = House
    list_display = (
        "name", "latitude", "longitude",
        "price", "bedrooms", "bathrooms",
        "created", "updated",
    )
    search_fields = (
        'name',
    )
    list_filter = (
        "bedrooms", "bathrooms", "created", "updated",
    )
    readonly_fields = ("created", "updated", )

admin.site.register(House, HouseAdmin)