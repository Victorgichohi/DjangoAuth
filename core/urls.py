

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from django.conf.urls import url, include
from django.contrib import admin
from .views import home_page
from django.views.generic import TemplateView, RedirectView
from accounts.views import LoginView, RegisterView

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include(('accounts.urls','accounts') ,namespace='accounts')),
    # url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
