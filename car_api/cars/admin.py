from django.contrib import admin
from django.urls import path
from .models import Car, Brand, Model_Car

admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(Model_Car)