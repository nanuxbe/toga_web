from django.contrib import admin

from .models import CookBook, Recipe, Following


admin.site.register(CookBook)
admin.site.register(Recipe)
admin.site.register(Following)
