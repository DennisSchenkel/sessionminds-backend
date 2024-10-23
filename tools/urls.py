from django.urls import path
from tools import views

urlpatterns = [
    path("", views.ToolList.as_view()),
    path(
        "user/<int:user_id>/",
        views.ToolListByUser.as_view(),
        name="tools-by-user"
        ),
    path(
        "<int:id>/",
        views.ToolDetailById.as_view(),
        name="tool-detail"
        ),
    path(
        "tool/<slug:slug>/",
        views.ToolDetailBySlug.as_view(),
        name="tool-detail"
        ),
]
