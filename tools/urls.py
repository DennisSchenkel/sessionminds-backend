from django.urls import path
from tools import views

urlpatterns = [
    path("tools/", views.ToolList.as_view()),
    path("tools/tool/<slug:slug>/", views.ToolDetail.as_view(), name="tool-detail"),
]
