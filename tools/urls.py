from django.urls import path
from tools import views

urlpatterns = [
    path('tools/', views.ToolList.as_view()),
    path('tools/tool/<slug:slug>/', views.ToolDetail.as_view()),
    path('tools/create/', views.ToolCreate.as_view()),
    path('tools/update/<int:id>/', views.ToolUpdate.as_view()),
]
