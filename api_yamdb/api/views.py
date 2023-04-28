from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category, Comment, Review
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer,)
from .permissions import ReadOnly, IsAuthor, IsAdmin, IsModerator


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [ReadOnly | IsAuthor | IsAdmin | IsModerator]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genres__slug', 'year', 'category__slug', 'name')

    def perform_create(self, serializer):
        genres = self.request.data.getlist('genre')
        category = self.request.data.get('category')
        serializer.save(genres=genres, category=category)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly | IsAuthor | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review__id=review_id,
                                      review__title__id=title_id)

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
        return Review.objects.filter(title__id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        title=title)
