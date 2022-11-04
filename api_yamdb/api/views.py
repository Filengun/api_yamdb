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

from api_yamdb.services import send_confirmation_code


from django.shortcuts import render
from .serializers import CategorySerializer, GenreSerializer, TitleListSerializer, TitleCreateSerializer
from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework import permissions


class UserSignupView(GenericAPIView):
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email,
            confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTokenView(GenericAPIView):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response({'confirmation_code': 'неверный код'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'token': str(AccessToken.for_user(user))},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UsersSerializer
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
 
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