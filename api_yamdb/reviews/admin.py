from django.contrib import admin
from .models import Genre, Category, Title, Comment, Review #Comment, Review,


admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Review)
