from django.urls import path
from categories import views

urlpatterns = [
    path('categories/', views.CategoriesList.as_view()),
    path('categories/<int:id>/', views.CategoryDetail.as_view()),
]
