from django.urls import include, path
from rest_framework import routers

from api.views import UserViewSet, UserSignupView, UserGetTokenView, CategoryViewSet, TitleViewSet, GenreViewSet, ReviewViewSet, CommentViewSet 

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls), name='api-root'),
    path('v1/auth/signup/', UserSignupView.as_view()),
    path('v1/auth/token/', UserGetTokenView.as_view())
]
