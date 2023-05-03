from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category, Comment, Review
from .serializers import (TitleReadSerializer, TitleWriteSerializer,
                          GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer,)
from .permissions import ReadOnly, IsAuthor, IsAdmin, IsModerator
from reviews.filters import TitleFilter


class CreateListDestroyMixin(mixins.CreateModelMixin, mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """Миксин на создание, удаление и получение списка объектов."""

    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id')
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly | IsAuthor | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(
            review__id=review_id, review__title__id=title_id).order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs['review_id']
        review = get_object_or_404(title.reviews, id=review_id)

        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReadOnly | IsAuthor | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title__id=title_id).order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        title=title)
