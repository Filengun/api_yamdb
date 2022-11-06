from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (TokenSerializer, UsersSerializer)
from users.models import User
from django.contrib.auth.tokens import default_token_generator

from rest_framework.filters import SearchFilter
from .filters import TitlesFilter
from .permissions import (
    IsAdminOrSuperUser,
    IsAdminOrReadOnly,
    IsAuthUserOrAuthorOrModerOrAdmin
)
from django.db.models import Avg

from api_yamdb.services import send_confirmation_code

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleListSerializer,
    TitleCreateSerializer,
    UserPersonalDataSerializer,
    UserSignUpSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework import permissions


class UserSignupView(GenericAPIView):
    serializer_class = UserSignUpSerializer
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
        serializer_class=UserPersonalDataSerializer
    )
    def about_me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """Категории. GET, POST, DEL."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    filter_backends = [SearchFilter]
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)

    @action(
        detail=False,
        methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug',
    )
    def delete_category(self, request, slug):
        category = self.get_object()
        serializer = self.get_serializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    """Жанр. GET, POST, DEL."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)
    filter_backends = [SearchFilter]
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)

    @action(
        detail=False,
        methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug',
    )
    def delete_genre(self, request, slug):
        category = self.get_object()
        serializer = self.get_serializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения.GET, POST, PATCH, DEL."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    filter_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthUserOrAuthorOrModerOrAdmin,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Возвращает queryset c отзывами для произведения."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthUserOrAuthorOrModerOrAdmin,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
