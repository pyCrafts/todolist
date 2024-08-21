import rest_framework.permissions as permissions
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from goals.serializers import (GoalCategoryCreateSerializer,
                               GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, GoalCommentSerializer,
                               GoalCommentCreateSerializer)
from goals.models import Goal, GoalCategory, GoalComment
from django.db.models import Q


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']
    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
       instance.is_deleted = True
       instance.save(update_fields=('is_deleted',))
       return instance


class GoalCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    ordering_fields = ["title", 'created']
    ordering = ["title"]
    search_fields = ["title", "description"]
    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id)
            & ~Q(status=Goal.Status.archived)
        )
    

class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Goal.objects.filter(Q(user_id=self.request.user.id)
            & ~Q(status=Goal.Status.archived)
        )
    

class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ["-created"]
   
    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)
    

class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Goal.objects.filter(Q(user_id=self.request.user.id)
            & ~Q(status=Goal.Status.archived)
        )