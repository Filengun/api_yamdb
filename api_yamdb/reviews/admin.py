from django.contrib import admin
from .models import Genre, Category, Title, Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_filter = ('pub_date',)
    search_fields = ('text',)
    empty_value_display = '-none-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'review',
        'pub_date'
    )
    list_filter = ('pub_date',)
    search_fields = ('text',)
    empty_value_display = '-none-'


admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
