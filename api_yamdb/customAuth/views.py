from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import SignupSerializer, TokenSerializer
from .utils import generate_confirmation_code


class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        confirmation_code = generate_confirmation_code()

        user = serializer.save(
            username=username,
            email=email,
            confirmation_code=confirmation_code,
        )

        user.set_password(password)
        user.save()

        send_mail(
            'Confirmation code',
            f'Confirmation code: {confirmation_code}',
            'from@admins.com',
            [email],
            fail_silently=False,
        )
        return Response({'detail': 'Confirmation code sent'}, status=status.HTTP_201_CREATED)


class TokenObtainPairView(APIView):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_201_CREATED)
