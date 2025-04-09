from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

def index(request):
    return render(request, "layout.html")

urlpatterns = [
    path("", index, name="index"),
    path("home/", index, name="home"),  # Thêm tuyến đường /home/
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path("api/users/", include("users.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)