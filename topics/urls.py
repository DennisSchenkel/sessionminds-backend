from django.urls import path
from topics import views

urlpatterns = [
    path("topics/", views.TopicsList.as_view()),
    path("topics/<slug:slug>/", views.TopicDetail.as_view()),
    path("topics/<id>/", views.TopicDetailById.as_view()),
]
