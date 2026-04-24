from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .serializers import UsuarioSerializer, ClienteSerializer, SeguroSerializer, DoctorSerializer, NecesidadSerializer, SemanaSerializer
from .models import Cliente, Seguro, Doctor, Necesidad, Semana





class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_anonymous:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        elif request.user.is_staff or request.user.is_superuser:
            is_staff = request.data.get('is_staff', True)
            is_superuser = request.data.get('is_superuser', False)
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=is_staff,
                is_superuser=is_superuser
            )

        else:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        return Response(
            UsuarioSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
   
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def perfil(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SemanaViewSet(viewsets.ModelViewSet):
    queryset = Semana.objects.all()
    serializer_class = SemanaSerializer


class ClienteViewSet(viewsets.ModelViewSet): #ruta para manejar los clientes, se pueden crear, actualizar, eliminar y listar clientes
    queryset = Cliente.objects.all()            #es decir, es similar a un listview, pero con mas funcionalidades
    serializer_class = ClienteSerializer

    @action(detail=True, methods=['get']) #ruta personalizada para obtener los dependientes de un cliente
    def dependientes(self, request, pk=None):
        cliente = self.get_object()
        dependientes = cliente.dependientes.all()
        serializer = self.get_serializer(dependientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get']) #ruta personalizada para obtener los seguros de un cliente
    def seguros(self, request, pk=None):
        cliente = self.get_object()
        seguros = cliente.seguros.all()
        serializer = SeguroSerializer(seguros, many=True)
        return Response(serializer.data)


class SeguroViewSet(viewsets.ModelViewSet): #ruta para manejar los seguros, se pueden crear, actualizar, eliminar y listar seguros
    queryset = Seguro.objects.all()
    serializer_class = SeguroSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class NecesidadViewSet(viewsets.ModelViewSet):
    queryset = Necesidad.objects.all()
    serializer_class = NecesidadSerializer

    @action(detail=True, methods=['get'])
    def doctores_especialidad(self, request, pk=None):
        necesidad = self.get_object()
        doctores = necesidad.doctor_especialidad.all()
        serializer = DoctorSerializer(doctores, many=True)
        return Response(serializer.data)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_anonymous:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        elif request.user.is_staff or request.user.is_superuser:
            is_staff = request.data.get('is_staff', True)
            is_superuser = request.data.get('is_superuser', False)
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=is_staff,
                is_superuser=is_superuser
            )

        else:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        return Response(
            UsuarioSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
   
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def perfil(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
