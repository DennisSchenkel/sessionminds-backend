from django.urls import path
from tools import views

urlpatterns = [
    path('tools/', views.ToolList.as_view()),
    path('tools/<slug:slug>/', views.ToolDetail.as_view()),
]
