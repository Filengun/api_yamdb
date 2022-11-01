from django.contrib import admin
from .models import Genre, Category, Title #Comment, Review,

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
