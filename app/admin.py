from django.contrib import admin
from .models import Producto
# Register your models here.


class productadmin(admin.ModelAdmin):
    list_display = ["artista","nombreprod","precio"]
    list_editable= ["precio"]
    search_fields=["artista"]


admin.site.register(Producto,productadmin)