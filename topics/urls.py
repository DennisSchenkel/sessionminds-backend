from django.urls import path
from topics import views

urlpatterns = [
    path("", views.TopicsList.as_view()),
    path("<slug:slug>/", views.TopicDetailsBySlug.as_view()),
    path("list/<slug:slug>/", views.ToolsOfTopicBySlug.as_view()),
]
