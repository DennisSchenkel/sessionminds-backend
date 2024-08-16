from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route

urlpatterns = [
    path("", root_route),
    path("admin/", admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path("logout/", logout_route),
    path("", include("profiles.urls")),
    path("", include("categories.urls")),
    path("", include("tools.urls")),
]
