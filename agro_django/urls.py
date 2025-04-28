from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls

from payments.unfold.sites import payments_admin_site

urlpatterns = [
    path("admin/", payments_admin_site.urls),
    path("cms/", include(wagtailadmin_urls)),
]
