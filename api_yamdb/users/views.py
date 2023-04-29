from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import User, UserSerializer, SignupSerializer, TokenSerializer
from .permissions import IsAdminOrYourself


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrYourself,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    lookup_field = 'username'
    search_fields = ('username',)
    ordering = ('username',)

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            return self.request.user
        return super().get_object()

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).first():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.kwargs.get('username') != 'me' and request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, created = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username')
        )

        user.confirmation_code = default_token_generator.make_token(user)
        user.save(update_fields=['confirmation_code'])

        send_mail(
            'Confirmation code',
            f'Confirmation code: {user.confirmation_code}',
            'from@admins.com',
            [user.email],
            fail_silently=False,
        )

        return Response({
            'email': user.email,
            'username': user.username
        }, status=status.HTTP_200_OK)


class TokenObtainPairView(APIView):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        if not default_token_generator.check_token(user, confirmation_code):
            return Response({'confirmation_code': 'Неправильный код подтверждения'},
                            status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
