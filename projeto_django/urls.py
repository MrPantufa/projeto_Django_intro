from django.contrib import admin
from django.urls import path
from core.views import index, contador_page, async_tick

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('contador/', contador_page, name='contador_page'),
    path('api/tick/', async_tick, name='async_tick'),
]
