from django.urls import path, include
from rest_framework.routers import DefaultRouter

from customAuth.views import SignupView, TokenObtainPairView
from users.views import UserViewset
from .views import ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()
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