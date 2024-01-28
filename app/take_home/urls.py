from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from take_home.views import BookViewSet
from django.contrib import admin
from take_home import views

schema_view = get_schema_view(
   openapi.Info(
      title='Books API',
      default_version='v1',
      description='Emotive Backend Challenge',
   ),
   public=True,
)

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
