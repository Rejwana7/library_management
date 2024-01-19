"""
URL configuration for batighar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from core.views import Homeview
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",Homeview.as_view(),name="homepage"),
    path('category/<slug:category_slug>/',Homeview.as_view(),name="category_wise_book"),
    path("account/",include("account.urls")),
    path("transaction/",include("transaction.urls")),
    path("book/",include("book.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
