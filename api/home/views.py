from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import TodoSerializer
from .models import Todo
from .paginations import CustomPageNumberPagination, has_pagination, no_pagination
from .permissions import AddTodo

# Create your views here.
class TodoPageView(APIView, PageNumberPagination):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination = True

    _paginationClass = CustomPageNumberPagination
    _serializerClass = TodoSerializer
    _modelClass = Todo

    def paginate_queryset(self, data):
        return self._paginationClass().paginate_queryset(data, self.request, view=self)

    def get_object(self):
        try:
            return self._modelClass.objects.all()
        except self._modelClass.DoesNotExist:
            raise Http404

    def serializer(self, data):
        return self._serializerClass(data, many=True)

    def get(self, request):
        currentPage = int(request.GET.get("page", 1))
        if currentPage > 0:
            todoItem = self.get_object()
            todoItemPaginate = self.paginate_queryset(todoItem)
            todoItemSerializer = self.serializer(todoItemPaginate)

            totalItem = todoItem.count()

            result = {
                "items": todoItemSerializer.data,
                "pagination": has_pagination(request, totalItem)
                if self.pagination
                else no_pagination(),
            }
        else:
            result = {
                "items": [],
                "pagination": no_pagination(),
            }
        return Response(result)


class TodoAddItem(APIView):
    permission_classes = [
        AddTodo,
    ]
    _serializerClass = TodoSerializer

    def post(self, request):
        todoItemSerializer = self._serializerClass(data=request.data)
        if todoItemSerializer.is_valid():
            todoItemSerializer.save()
            return Response("created successfully")
        else:
            return Response("data is not valid")


class TodoDetail(APIView):
    # https://stackoverflow.com/questions/58099040/django-permission-required
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    _modelClass = Todo
    _serializerClass = TodoSerializer

    def get_object(self, pk):
        try:
            return self._modelClass.objects.get(pk=pk)
        except self._modelClass.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = self._serializerClass(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = self._serializerClass(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("updated successfully", status=status.HTTP_200_OK)
        return Response("updated failed", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response("deleted successfully", status=status.HTTP_200_OK)
