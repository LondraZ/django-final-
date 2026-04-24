from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from cuentas.views import UsuarioViewSet, DoctorViewSet, ClienteViewSet, NecesidadViewSet, SeguroViewSet, SemanaViewSet
from chatbot.views import ChatbotView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('usuario', UsuarioViewSet, basename='usuarios')
router.register('doctores', DoctorViewSet, basename='doctores')
router.register('semanas', SemanaViewSet, basename='semanas')
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('necesidades', NecesidadViewSet, basename='necesidades')
router.register('seguros', SeguroViewSet, basename='seguros')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cuentas/', include('cuentas.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/chatbot/', ChatbotView.as_view(), name="chatbot"),
    path('api/', include(router.urls))
]
