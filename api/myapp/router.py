from rest_framework import routers
from home.views import TodoView

router = routers.SimpleRouter()
router.register("todo", TodoView, basename="todo")
urlpatterns = router.urls
