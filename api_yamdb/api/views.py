from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = []
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'year', 'category__slug', 'name')

    def perform_create(self, serializer):
        genre = self.request.data.get('genre')
        category = self.request.data.get('category')
        serializer.save(genre=genre, category=category)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
