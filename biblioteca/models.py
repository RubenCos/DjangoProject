from django.db import models


class Libro(models.Model):
    GENEROS = [
        ('ficcion', 'Ficción'),
        ('no_ficcion', 'No Ficción'),
        ('ciencia', 'Ciencia'),
        ('historia', 'Historia'),
        ('biografia', 'Biografía'),
        ('fantasia', 'Fantasía'),
        ('terror', 'Terror'),
        ('romance', 'Romance'),
        ('infantil', 'Infantil'),
        ('otro', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, default='')
    genero = models.CharField(max_length=50, choices=GENEROS, default='otro')
    anio_publicacion = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True, default='')
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return f"{self.titulo} - {self.autor}"