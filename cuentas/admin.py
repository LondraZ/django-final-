from django.contrib import admin
from cuentas.models import Cliente, Seguro, Doctor, Necesidad, Semana

# Register your models here.

@admin.register(Semana)
class SemanaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'descripcion']
    list_filter = ['numero']
    search_fields = ['numero', 'descripcion']


class SeguroInline(admin.TabularInline):
    model = Seguro
    extra = 0
    fields = ['aseguradora', 'plan', 'numero_poliza']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    inlines = [SeguroInline]
    list_display = ['primer_nombre', 'primer_apellido', 'telefono_formateado', 'estado', 'get_semanas', 'seguros_info', 'relacionado_con']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['primer_nombre', 'primer_apellido', 'telefono']

    def get_semanas(self, obj):
        return ", ".join([str(s.numero) for s in obj.semanas.all()])
    get_semanas.short_description = 'Semanas'


@admin.register(Seguro)
class SeguroAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'aseguradora', 'numero_poliza', 'plan']
    list_filter = ['aseguradora', 'fecha_creacion']
    search_fields = ['cliente__primer_nombre', 'cliente__primer_apellido', 'numero_poliza']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especialidad', 'telefono_formateado', 'clinica_hospital']
    list_filter = ['especialidad', 'fecha_creacion']
    search_fields = ['nombre', 'clinica_hospital']


@admin.register(Necesidad)
class NecesidadAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'descripcion', 'semana', 'estado', 'doctor_primario', 'especialidad','fecha_cita']
    list_filter = ['estado', 'semana', 'fecha_cita', 'fecha_creacion']
    search_fields = ['cliente__primer_nombre', 'cliente__primer_apellido', 'descripcion']


