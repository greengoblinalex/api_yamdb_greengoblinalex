from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from reviews.models import Title, Genre, Category

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = []  # добавить права доступа
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'year', 'category__slug', 'name')

    def perform_create(self, serializer):
        genre = self.request.data.get('genre')
        category = self.request.data.get('category')
        serializer.save(genre=genre, category=category)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []  # добавить права доступа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []  # добавить права доступа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'
