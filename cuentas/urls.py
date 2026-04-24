from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('usuario', views.UsuarioViewSet, basename='usuarios')
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'seguros', views.SeguroViewSet)
router.register(r'doctores', views.DoctorViewSet)
router.register(r'necesidades', views.NecesidadViewSet)
router.register(r'semanas', views.SemanaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)),
]