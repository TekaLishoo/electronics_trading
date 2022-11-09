"""electronics_trading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from src.electronics.views import NetworkObjectsViewSet

schema_view = get_schema_view(
    title="A Different API", renderer_classes=[CoreJSONRenderer]
)

router = routers.SimpleRouter()
router.register(r"networkobjects", NetworkObjectsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chaining/", include("smart_selects.urls")),
    path("api/", include(router.urls)),
    path("swagger/", schema_view),
]
