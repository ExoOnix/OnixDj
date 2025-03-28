from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Ensure only authenticated users can access this view

    def get_queryset(self):
        # Return only the todos belonging to the authenticated user
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the new Todo with the authenticated user
        serializer.save(user=self.request.user)
