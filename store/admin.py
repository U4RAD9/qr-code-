from django.contrib import admin
from .models.customer import Users
from .models.location import Location

# Register your models here.

admin.site.register(Users)
admin.site.register(Location)
