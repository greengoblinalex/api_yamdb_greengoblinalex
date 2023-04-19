from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                'reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                CommentViewSet, 'comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
