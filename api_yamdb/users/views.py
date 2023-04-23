from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer, User
from .permissions import IsAdminOrYourself


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrYourself,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'username'
    filterset_fields = ('username',)

    def get_object(self):
        if self.kwargs['username'] == 'me':
            return self.request.user
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.kwargs['username'] != 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
