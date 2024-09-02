from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
    TokenBlacklistView
)
from .views import root_route

urlpatterns = [
    path("", root_route),
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/",
         TokenObtainPairView.as_view(),
         name="token_obtain_pair"
         ),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh"
         ),
    path("api/token/blacklist/",
         TokenBlacklistView.as_view(),
         name="token_blacklist"
         ),
    path("", include("profiles.urls")),
    path("", include("topics.urls")),
    path("", include("tools.urls")),
    path("", include("votes.urls")),
]
