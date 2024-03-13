from django.contrib import admin
from django.urls import path, include

from core.views import frontpage, about

urlpatterns = [
    path('about/', about, name='about'),
    path('', frontpage, name='frontpage'),
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
]
