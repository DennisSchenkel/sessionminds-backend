from django.urls import path
from profiles import views

urlpatterns = [
    path("profiles/", views.ProfileList.as_view()),
    path("profiles/<int:id>/", views.ProfileDetail.as_view()),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]
