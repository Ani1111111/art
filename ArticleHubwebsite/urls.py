
from django.contrib import admin
from django.urls import path
from django.urls.conf import include 
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from ArticleHubwebsite import settings
admin.site.site_header = "ArtHub Admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('articles/', include('articles.urls')),
    path('',RedirectView.as_view(url="articles/")),
    path('oauth/',include('social_django.urls',namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
