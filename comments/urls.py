from django.urls import path
from comments import views

urlpatterns = [
    path(
        "comments/tool/<int:id>/",
        views.ToolComments.as_view(),
        name="tool-comments"
        ),
    path(
        "comments/<int:id>/",
        views.CommentDetails.as_view(),
        name="comment-details"
        ),
]
