from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdminOrSuperUser
from api.serializers import (TokenSerializer, UsersSerializer)
from users.models import User
from django.contrib.auth.tokens import default_token_generator

from rest_framework.filters import SearchFilter
from .filters import TitlesFilter

from api_yamdb.services import send_confirmation_code


from django.shortcuts import render
from .serializers import CategorySerializer, GenreSerializer, TitleListSerializer, TitleCreateSerializer
from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework import permissions

class CategoryViewSet(viewsets.ModelViewSet):
    """Категория,."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    filter_backends = [SearchFilter]


class GenreViewSet(viewsets.ModelViewSet):
    """Жанр, ."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)
    filter_backends = [SearchFilter]

class TitleViewSet(viewsets.ModelViewSet):
    """Произведения, ."""
    queryset = Title.objects.all()
    filter_class = TitlesFilter
    # serializer_class = TitleListSerializer
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleListSerializer
        return TitleCreateSerializer


