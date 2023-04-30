from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from reviews.filters import TitleFilter
from reviews.models import Title, Genre, Category, Review
from .permissions import ReadOnly, IsAuthor, IsAdmin, IsModerator
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer, )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def list(self, request, *args, **kwargs):
        titles = self.filter_queryset(self.get_queryset())

        titles_page = self.paginate_queryset(titles)
        serializer = self.get_serializer(titles_page, many=True)
        titles_serializer_data = serializer.data

        average_ratings = (
            Review.objects
            .filter(title__in=titles_page)
            .values('title')
            .annotate(rating=Avg('score'))
            .order_by('title')
        )

        for title, average_rating in zip(
                titles_serializer_data, average_ratings
        ):
            title['rating'] = (
                    average_rating['rating'] and int(average_rating['rating'])
            )

        return self.get_paginated_response(titles_serializer_data)

    def retrieve(self, request, *args, **kwargs):
        title = self.get_object()
        serializer = self.get_serializer(title)
        title_serializer_data = serializer.data

        average_rating = (
            Review.objects
            .filter(title=title)
            .aggregate(rating=Avg('score'))
        )

        title_serializer_data['rating'] = (
                average_rating['rating'] and int(average_rating['rating'])
        )

        return Response(title_serializer_data)

    def perform_create(self, serializer):
        genres = self.request.data.getlist('genre')
        category = self.request.data.get('category')
        serializer.save(genre=genres, category=category)

    def perform_update(self, serializer):
        genres = self.request.data.getlist('genre')
        category = self.request.data.get('category')
        serializer.save(genre=genres, category=category)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
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
    permission_classes = [ReadOnly | IsAuthor | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title__id=title_id).order_by('id')

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
