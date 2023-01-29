from django.urls import path
from .views import TodoPageView, TodoAddItem, TodoDetail

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("list/", TodoPageView.as_view()),
    path("add/", TodoAddItem.as_view()),
    path("detail/<int:pk>/", TodoDetail.as_view()),
]
