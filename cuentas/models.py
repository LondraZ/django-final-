from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.

class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Semana(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=100, blank=True)

class Cliente(BaseModel):
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    Email = models.CharField(max_length=255, blank=True, null=True)
    Seguro_social = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=6)
    estado = models.CharField(max_length=100)
    relacionado_con = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dependientes'
    )
    semanas = models.ManyToManyField(Semana, blank=True, related_name='clientes')

    @property
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    @property
    def telefono_formateado(self):
        if self.telefono and len(self.telefono) == 10:
            return f"({self.telefono[:3]}) {self.telefono[3:6]} {self.telefono[6:]}"
        return self.telefono

    @property
    def seguros_info(self):
        seguros = self.seguros.all()
        if not seguros:
            return '-'
        return ' | '.join(
            f"{seg.aseguradora} - {seg.plan} - {seg.numero_poliza}" for seg in seguros
        )

    def clean(self):
        if self.telefono and len(self.telefono.strip()) != 10:
            raise ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        if self.telefono and not self.telefono.isdigit():
            raise ValidationError('El teléfono solo puede contener números.')

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

    class Meta:
        ordering = ['primer_apellido', 'primer_nombre']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Seguro(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='seguros')
    aseguradora = models.CharField(max_length=150)
    numero_poliza = models.CharField(max_length=50, blank=True, null=True)
    plan = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.aseguradora}"

    class Meta:
        ordering = ['aseguradora']
        verbose_name = "Seguro"
        verbose_name_plural = "Seguros"


class Doctor(BaseModel):
    nombre = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=120, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    clinica_hospital = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    seguros = models.ManyToManyField(Seguro, blank=True, related_name='doctores')

    @property
    def telefono_formateado(self):
        if self.telefono and len(self.telefono) == 10:
            return f"({self.telefono[:3]}) {self.telefono[3:6]} {self.telefono[6:]}"
        return self.telefono

    def clean(self):
        if self.telefono and len(self.telefono.strip()) != 10:
            raise ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        if self.telefono and not self.telefono.isdigit():
            raise ValidationError('El teléfono solo puede contener números.')

    def __str__(self):
        partes = [self.nombre]
        if self.especialidad:
            partes.append(self.especialidad)
        if self.ciudad:
            partes.append(self.ciudad)
        return ' - '.join(partes)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"


class Necesidad(BaseModel):
    ESTADO_CHOICES = (
        ('esperando', 'Esperando Cita'),
        ('falta_informacion', 'Falta Informacion'),
        ('tratado', 'Tratado'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='necesidades')
    descripcion = models.CharField(max_length=255)
    fecha_cita = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='esperando')
    doctor_primario = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True, related_name='necesidades_primarias')
    semana = models.ForeignKey(Semana, on_delete=models.SET_NULL, blank=True, null=True, related_name='necesidades')
    especialidad = models.CharField(max_length=120, blank=True, null=True)
    doctor_especialidad = models.ManyToManyField(Doctor, blank=True, related_name='necesidades_especialidad')
    notas = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs): #este metodo se ejecuta cada vez que se guarda un objeto de esta clase, es decir, cada vez que se crea o se actualiza una necesidad
        old_cliente = None           #es decir, si pongo un numero de semana, se actualiza en cliente
        old_semana = None
        if self.pk:
            try:
                old = Necesidad.objects.get(pk=self.pk)
                old_cliente = old.cliente
                old_semana = old.semana
            except Necesidad.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if self.semana and self.cliente:
            self.cliente.semanas.add(self.semana)

        if old_cliente and old_semana and (old_cliente != self.cliente or old_semana != self.semana):
            if not old_cliente.necesidades.filter(semana=old_semana).exclude(pk=self.pk).exists():
                old_cliente.semanas.remove(old_semana)

    def delete(self, *args, **kwargs):
        cliente = self.cliente
        semana = self.semana
        super().delete(*args, **kwargs)
        if cliente and semana and not cliente.necesidades.filter(semana=semana).exists():
            cliente.semanas.remove(semana)

    def __str__(self):
        doctor = self.doctor_primario.nombre if self.doctor_primario else 'Sin doctor'
        return f"{self.cliente} - {self.descripcion} ({self.get_estado_display()}) - {doctor}"

    class Meta:
        ordering = ['-fecha_cita']
        verbose_name = "Necesidad Médica"
        verbose_name_plural = "Necesidades Médicas"
