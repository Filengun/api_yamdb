from reviews.models import Category, Genre, Title
from rest_framework import serializers
from users.models import User


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
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


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        """Проверяет чтобы username был не меньше 3 символов."""
        if len(username) < 3:
            raise serializers.ValidationError(
                'Username должен быть длиннее двух символов.'
            )
        return username

    def validate_role(self, role):
        """Менять поле role разрешено только для админа и суперпользоватеня"""
        if not self.instance:
            return role
        if self.instance.role == 'admin' or self.instance.is_superuser:
            return role
        return self.instance.role


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
