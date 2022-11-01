from reviews.models import Category, Genre, Title
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории"""
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра"""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre

class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор получения списка произведений"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',)
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания произведения"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title