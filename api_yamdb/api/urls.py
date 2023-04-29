from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewset, SignupView, TokenObtainPairView
from .views import (ReviewViewSet, CommentViewSet,
                    TitleViewSet, GenreViewSet, CategoryViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'users', UserViewset, basename='users')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   'reviews')
router_v1.register((r'titles/(?P<title_id>\d+)/reviews/'
                    r'(?P<review_id>\d+)/comments'),
                   CommentViewSet, 'comments')

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token'),
    path('v1/', include(router_v1.urls))

]
