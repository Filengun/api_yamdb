from django.shortcuts import render
from .serializers import CategorySerializer, GenreSerializer, TitleListSerializer, TitleCreateSerializer
from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework import permissions
#фильтры?
class CategoryViewSet(viewsets.ModelViewSet):
    """Категория,."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)

class GenreViewSet(viewsets.ModelViewSet):
    """Жанр, ."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)

class TitleViewSet(viewsets.ModelViewSet):
    """Произведения, ."""
    queryset = Title.objects.all()
    # serializer_class = TitleListSerializer
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleListSerializer
        return TitleCreateSerializer
    


