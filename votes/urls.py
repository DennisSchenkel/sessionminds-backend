from django.urls import path
from votes import views


urlpatterns = [
    path("", views.VoteList.as_view()),
    path("<int:pk>/", views.VoteDetails.as_view(), name="vote-details"),
    path("tool/<int:id>/", views.VotesByTool.as_view()),
]
