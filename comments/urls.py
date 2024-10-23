from django.urls import path
from comments import views

urlpatterns = [
    path(
        "tool/<int:id>/",
        views.ToolComments.as_view(),
        name="tool-comments"
        ),
    path(
        "<int:id>/",
        views.CommentDetails.as_view(),
        name="comment-details"
        ),
]
