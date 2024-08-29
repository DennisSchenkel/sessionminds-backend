from django.urls import path
from categories import views

urlpatterns = [
    path("categories/", views.CategoriesList.as_view()),
    path("categories/<slug:slug>/", views.CategoryDetail.as_view()),
    path("category/<id>/", views.CategoryDetailById.as_view()),
]
