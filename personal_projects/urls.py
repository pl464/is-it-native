"""personal_projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Use include() to add paths from the catalog application
from django.urls import include
#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robin/', include('robin_scraper.urls')),
    path('', RedirectView.as_view(url='robin/', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static
#allows serving of css js and images
#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
