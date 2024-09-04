from django.urls import path
from topics import views

urlpatterns = [
    path("topics/", views.TopicsList.as_view()),
    path("topics/<slug:slug>/", views.TopicDetailsBySlug.as_view()),
    path("topics/<id>/", views.TopicDetailsById.as_view()),
]