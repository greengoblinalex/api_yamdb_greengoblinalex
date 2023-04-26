from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from customAuth.serializers import SignupSerializer, TokenSerializer
from django.contrib.auth.tokens import default_token_generator
from .models import User


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
