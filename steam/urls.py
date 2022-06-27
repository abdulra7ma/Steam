from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import SimpleRouter
from account.views import FollowViewSet
from games.views import GameViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = SimpleRouter()
router.register('games', GameViewSet)
# router.register('followers', FollowViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('account/', include('account.urls')),
   path('cart/', include('cart.urls')),
   path('api/', include(router.urls)),
   path('admin/', admin.site.urls),
   path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
