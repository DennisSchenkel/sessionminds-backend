from django.urls import path
from tools import views

urlpatterns = [
    path("tools/", views.ToolList.as_view()),
    path(
        "tools/user/<int:user_id>/",
        views.ToolListByUser.as_view(),
        name="tools-by-user"
        ),
    path(
        "tools/<int:id>/",
        views.ToolDetailById.as_view(),
        name="tool-detail"
        ),
    path(
        "tools/tool/<slug:slug>/",
        views.ToolDetailBySlug.as_view(),
        name="tool-detail"
        ),
]
