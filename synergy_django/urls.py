from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    path('api/', include('contents.urls')),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
