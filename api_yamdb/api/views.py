from typing import Optional

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.filters import TitleFilter
from reviews.models import Title, Genre, Category, Review
from .permissions import IsAuthor, IsAdmin, IsModerator, ReadOnly
from .serializers import (TitleReadSerializer, TitleWriteSerializer,
                          GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer, )


class CreateListDestroyMixin(mixins.CreateModelMixin, mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """Миксин на создание, удаление и получение списка объектов."""

    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id')
    permission_classes = [IsAdmin | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer

    def list(self, request, *args, **kwargs):
        titles = self.filter_queryset(self.get_queryset())

        titles_page: list[Title] = self.paginate_queryset(titles)
        serializer = self.get_serializer(titles_page, many=True)
        titles_serializer_data: dict = serializer.data

        average_ratings: dict = (
            Review.objects
            .filter(title__in=titles_page)
            .values('title')
            .annotate(rating=Avg('score'))
            .order_by('title')
            .values('rating')
        )

        for title, average_rating in zip(
                titles_serializer_data, average_ratings
        ):
            title['rating']: Optional[int] = (
                    average_rating['rating'] and int(average_rating['rating'])
            )

        return self.get_paginated_response(titles_serializer_data)

    def retrieve(self, request, *args, **kwargs):
        title = self.get_object()
        serializer = self.get_serializer(title)
        title_serializer_data: dict = serializer.data

        average_rating: dict[str: float] = (
            Title.objects
            .annotate(rating=Avg('reviews__score'))
            .values('rating')
            .get(id=title.id)
        )
        title_serializer_data['rating']: Optional[int] = (
                average_rating['rating'] and int(average_rating['rating'])
        )

        return Response(title_serializer_data)


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']

        title = get_object_or_404(
            Title.objects.prefetch_related('reviews', 'reviews__comments'),
            id=title_id
        )

        return title.reviews.get(id=review_id).comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs['review_id']
        review = get_object_or_404(title.reviews, id=review_id)

        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title__id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_serializer_context(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)

        context = super().get_serializer_context()
        context.update({"title": title, 'author': self.request.user})
        return context
