from rest_framework import serializers
from django.contrib.auth.models import User
from cuentas.models import Cliente, Seguro, Doctor, Necesidad, Semana

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semana
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()
    telefono_formateado = serializers.ReadOnlyField()
    semanas = SemanaSerializer(many=True, read_only=True)
    seguros_info = serializers.ReadOnlyField()

    class Meta:
        model = Cliente
        fields = '__all__'


class SeguroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguro
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    telefono_formateado = serializers.ReadOnlyField()

    class Meta:
        model = Doctor
        fields = '__all__'


class NecesidadSerializer(serializers.ModelSerializer):
    semana = SemanaSerializer(read_only=True)
    doctor_primario = DoctorSerializer(read_only=True)
    doctor_especialidad = DoctorSerializer(many=True, read_only=True)

    class Meta:
        model = Necesidad
        fields = '__all__'
