from rest_framework import viewsets

from reviews.models import Comment, Review
from .serializers import (CommentSerializer, ReviewSerializer,)


class CommentViewSet(viewsets):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review__id=review_id,
                                      review__title__id=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title__id=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
