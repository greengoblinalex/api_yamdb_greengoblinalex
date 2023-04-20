from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignupViewSet, TokenObtainPairView

router_v1 = DefaultRouter()
router_v1.register(r'auth/signup', SignupViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token'),
]
