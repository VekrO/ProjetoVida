from django.contrib import admin
from .models import Ongs

@admin.register(Ongs)
class OngsAdmin(admin.ModelAdmin):
    pass