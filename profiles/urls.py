from django.urls import path
from profiles import views

urlpatterns = [
    path("users/", views.UsersListView.as_view(), name="user-list"),
    path(
        "users/<int:id>/",
        views.UserDetailView.as_view(),
        name="user-detail"
        ),
    path(
        "users/<int:id>/profile/",
        views.UserProfileView.as_view(),
        name="user-profile"
        ),
    path("users/<int:id>/delete/", views.UserDeleteView.as_view()),
    path("profiles/", views.ProfileList.as_view()),
    path("profiles/<int:id>/", views.ProfileDetail.as_view()),
    path("profiles/<slug:slug>/", views.UserProfileViewSlug.as_view()),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
]
