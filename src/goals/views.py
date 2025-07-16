import rest_framework.permissions as permissions
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from goals.permissions import (
    GoalCategoryPermissions,
    IsOwnerOrReadOnly,
    GoalPermissions,
    CommentPermissions,
    BoardPermissions,
)

from goals.serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalCreateSerializer,
    GoalSerializer,
    GoalCommentSerializer,
    GoalCommentCreateSerializer,
    BoardCreateSerializer,
    BoardListSerializer,
    BoardSerializer,
)
from goals.models import Goal, GoalCategory, GoalComment, Board
from django.db.models import Q


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["board"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related("board__participants").filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions, IsOwnerOrReadOnly]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related("board__participants").filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save(update_fields=("is_deleted",))
        return instance


class GoalCreateView(generics.CreateAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Goal.objects.select_related("user", "category__board").filter(
            Q(category__board__participants__user_id=self.request.user.id)
            & ~Q(status=Goal.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Goal.objects.select_related("user", "category__board").filter(
            Q(category__board__participants__user_id=self.request.user.id)
            & ~Q(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=("status",))
        return instance


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["goal"]
    ordering = ["-created"]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return GoalComment.objects.select_related(
            "goal__category__board", "user"
        ).filter(
            user_id=self.request.user.id,
            goal__category__board__participants__user_id=self.request.user.id,
        )


class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    ordering = ["title"]
    pagination_class = LimitOffsetPagination

    # filter_backends = [filters.OrderingFilter]
    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user_id=self.request.user.id, is_deleted=False
        )


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user_id=self.request.user.id, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save(update_fields=("is_deleted",))
        return instance
