import ast

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action


from .models import Todo, CustomUser
from .permissions import AddTodo, ViewTodo
from .serializers import TodoSerializer, LoginSerializer
from .paginations import CustomPageNumberPagination, has_pagination, no_pagination
from .custom_permission import CustomPermission

# Create your views here.
def get_user_token(request):
    try:
        token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
        return token
    except:
        return ""


def check_user_signature(request):
    token = get_user_token(request)
    if token != "":
        tokenSignature = token.split(".")[-1]
        if CustomUser.objects.filter(tokenSignature=tokenSignature).exists():
            return True
        return False
    return True


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

        if not check_user_signature(request):
            return HttpResponse("tai khoan da duoc dang nhap o noi khac")

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
            return Response("created success")
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


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    _userModel = CustomUser

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            # "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def handle_token(self, tokenAccess):
        return tokenAccess.split(".")[-1]

    def get_user(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        return user

    def update_user_signature(self, username, tokenSignature):
        return self._userModel.objects.filter(username=username).update(
            tokenSignature=tokenSignature
        )

    def post(self, request):
        jsonData = request.body
        stringData = jsonData.decode("utf-8")
        data = ast.literal_eval(stringData)
        username = data["username"]
        password = data["password"]

        user = self.get_user(request, username, password)
        if user is None:
            return Response("tai khoan khong ton tai")
        login(request, user)
        token = self.get_tokens_for_user(request.user)
        tokenSignature = self.handle_token(token["access"])
        self.update_user_signature(username, tokenSignature)
        return Response(token)


class Register(View):
    _userModel = CustomUser

    def create_user(self, username, password, email):
        return self._userModel.objects.create(username=username, email=email, password=password)

    def create_super_user(self, username, password, email):
        return self._userModel.objects.create(
            username=username, email=email, password=password, is_staff=True, is_superuser=True
        )

    def get(self, request):
        return render(request, "login/register.html")

    def post(self, request):
        userName = request.POST.get("username")
        if self._userModel.objects.filter(username=userName).exists():
            return HttpResponse("username " + userName + " da duoc su dung")

        userMail = request.POST.get("email")
        if self._userModel.objects.filter(email=userMail).exists():
            return HttpResponse("email " + userMail + " da duoc su dung")

        userPass = make_password(request.POST.get("password"))

        # user = CustomUser.objects.create(
        #     username=userName, email=userMail, password=userPass, is_staff=True, is_superuser=True
        # )
        user = self.create_user(userName, userPass, userMail)

        user.save()
        return HttpResponse("tao tai khoan thanh cong")


class TodoView(GenericViewSet):
    permission_classes = (CustomPermission,)
    _paginationClass = CustomPageNumberPagination
    serializer_class = TodoSerializer
    queryset = Todo.objects.all().order_by("id")

    def list(self, request):
        if not check_user_signature(request):
            return HttpResponse("tai khoan da duoc dang nhap o noi khac")
        todo = self._paginationClass().paginate_queryset(self.queryset, request, view=self)
        serializer = TodoSerializer(todo, many=True)

        totalItem = self.queryset.count()
        result = {"items": serializer.data, "pagination": has_pagination(request, totalItem)}
        return Response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(obj)
        return Response(serializer.data)

    @action(methods=["post"], detail=False, url_path="add")
    def add(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("create succes")
        return Response("data not valid")

    # @action(methods=["put"], detail=False, url_path="change")
    # def change(self, request, pk=None):
    #     obj = get_object_or_404(Todo, pk=request.data["id"])
    #     serializer = TodoSerializer(obj, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response("update successfully")
    #     return Response("update failed")

    @action(methods=["put"], detail=True, url_path="change")
    def change(self, request, pk=None):
        obj = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("update successfully")
        return Response("update failed")

    # http://localhost:8000/api1/todo/5/ vẫn xóa được
    @action(methods=["delete"], detail=True, url_path="delete_1")
    def delete(self, request, pk=None):
        obj = get_object_or_404(Todo, pk=pk)
        obj.delete()
        return Response("delete successfully")


class Token(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            # "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_user(self, request):
        token = get_user_token(request)
        tokenSignature = token.split(".")[-1]
        return CustomUser.objects.filter(tokenSignature=tokenSignature)

    def post(self, request):
        if not check_user_signature(request):
            return Response("da dang nhap noi khac")
        user = self.get_user(request)

        token = self.get_tokens_for_user(request.user)
        tokenSignature = token["access"].split(".")[-1]
        user.update(tokenSignature=tokenSignature)
        return Response(token)
