from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from src.electronics.views import (
    NetworkObjectsViewSet,
    NetworkObjectsBigDebtViewSet,
    ProductsViewSet,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    title="A Different API", renderer_classes=[CoreJSONRenderer]
)

router = routers.SimpleRouter()
router.register(r"networkobjects", NetworkObjectsViewSet)
router.register(r"networkobjects_bigdebt", NetworkObjectsBigDebtViewSet)
router.register(r"products", ProductsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chaining/", include("smart_selects.urls")),
    path("api/", include(router.urls)),
    path("swagger/", schema_view),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
