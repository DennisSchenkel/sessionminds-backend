from django.urls import path
from topics import views

urlpatterns = [
    path("topics/", views.TopicsList.as_view()),
    path("topics/<slug:slug>/", views.TopicDetailsBySlug.as_view()),
    path("topics/list/<slug:slug>/", views.ToolsOfTopicBySlug.as_view()),
]
