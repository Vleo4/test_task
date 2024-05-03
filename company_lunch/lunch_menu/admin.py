from django.contrib import admin
from .models import MealMenu, MenuUser

# Register your models here.
admin.site.register(MenuUser)
admin.site.register(MealMenu)