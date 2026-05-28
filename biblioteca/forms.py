from django import forms
from .models import Libro


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'descripcion', 'genero', 'anio_publicacion', 'isbn', 'disponible']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del libro'
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del autor'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción o sinopsis del libro'
            }),
            'genero': forms.Select(attrs={
                'class': 'form-select'
            }),
            'anio_publicacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2023',
                'min': 1000,
                'max': 2100
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (opcional)'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'descripcion': 'Descripción',
            'genero': 'Género',
            'anio_publicacion': 'Año de publicación',
            'isbn': 'ISBN',
            'disponible': 'Disponible',
        }


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Seleccionar archivo CSV',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )