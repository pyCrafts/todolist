from django.shortcuts import render
import rest_framework.permissions as permissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategory, GoalCategorySerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend


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
