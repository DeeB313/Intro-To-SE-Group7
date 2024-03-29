from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import frontpage, about
from django.views.generic.base import TemplateView

urlpatterns = [
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='core/robots.txt', content_type='text/plain')),
    path('', include("userprofile.urls")),
    path('', frontpage, name='frontpage'),
    path('', include('inventory.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
