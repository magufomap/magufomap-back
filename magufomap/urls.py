from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from api.router import router

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r"^api/", include(router.urls)),
    url(r"^api/login", obtain_jwt_token),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^magufomapadmin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
