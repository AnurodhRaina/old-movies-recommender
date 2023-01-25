from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard),
    path('info', views.info),
    path('table',views.Table, name = 'table')
]