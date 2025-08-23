from django.contrib import admin
from django.urls import path
from core.views import index, post_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    # nome da rota raiz ajustado para 'home' (usado em base.html)
    path('', index, name='home'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
]
