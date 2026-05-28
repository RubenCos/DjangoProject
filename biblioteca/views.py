import csv
import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from .models import Libro
from .forms import LibroForm, CSVImportForm


# ── Listado principal ─────────────────────────────────────────────────────────
def libro_list(request):
    query = request.GET.get('q', '')
    genero = request.GET.get('genero', '')
    disponible = request.GET.get('disponible', '')

    libros = Libro.objects.all()

    if query:
        libros = libros.filter(titulo__icontains=query) | libros.filter(autor__icontains=query)
    if genero:
        libros = libros.filter(genero=genero)
    if disponible == '1':
        libros = libros.filter(disponible=True)
    elif disponible == '0':
        libros = libros.filter(disponible=False)

    total = libros.count()
    disponibles = libros.filter(disponible=True).count()
    no_disponibles = libros.filter(disponible=False).count()

    context = {
        'libros': libros,
        'total': total,
        'disponibles': disponibles,
        'no_disponibles': no_disponibles,
        'query': query,
        'genero_sel': genero,
        'disponible_sel': disponible,
        'generos': Libro.GENEROS,
    }
    return render(request, 'biblioteca/libro_list.html', context)


# ── Detalle ───────────────────────────────────────────────────────────────────
def libro_detail(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'biblioteca/libro_detail.html', {'libro': libro})


# ── Crear ─────────────────────────────────────────────────────────────────────
def libro_create(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save()
            messages.success(request, f'✅ El libro "{libro.titulo}" ha sido añadido correctamente.')
            return redirect('libro_list')
    else:
        form = LibroForm()
    return render(request, 'biblioteca/libro_form.html', {'form': form, 'accion': 'Añadir'})


# ── Editar ────────────────────────────────────────────────────────────────────
def libro_edit(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ El libro "{libro.titulo}" ha sido actualizado.')
            return redirect('libro_list')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/libro_form.html', {'form': form, 'accion': 'Editar', 'libro': libro})


# ── Eliminar ──────────────────────────────────────────────────────────────────
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        titulo = libro.titulo
        libro.delete()
        messages.success(request, f'🗑️ El libro "{titulo}" ha sido eliminado.')
        return redirect('libro_list')
    return render(request, 'biblioteca/libro_confirm_delete.html', {'libro': libro})


# ── Exportar CSV ──────────────────────────────────────────────────────────────
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="biblioteca_{timestamp}.csv"'

    # BOM para compatibilidad con Excel
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['titulo', 'autor', 'descripcion', 'genero', 'anio_publicacion', 'isbn', 'disponible', 'fecha_creacion'])

    for libro in Libro.objects.all():
        writer.writerow([
            libro.titulo,
            libro.autor,
            libro.descripcion,
            libro.genero,
            libro.anio_publicacion or '',
            libro.isbn,
            'si' if libro.disponible else 'no',
            libro.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response


# ── Importar CSV ──────────────────────────────────────────────────────────────
def import_csv(request):
    form = CSVImportForm()

    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, '❌ El archivo debe tener extensión .csv')
                return render(request, 'biblioteca/csv_import.html', {'form': form})

            try:
                decoded = csv_file.read().decode('utf-8-sig')  # maneja BOM
                reader = csv.DictReader(io.StringIO(decoded))

                creados = 0
                errores = 0

                for fila in reader:
                    try:
                        disponible = fila.get('disponible', 'si').strip().lower() in ('si', 'sí', 'true', '1', 'yes')
                        anio_raw = fila.get('anio_publicacion', '').strip()
                        anio = int(anio_raw) if anio_raw.isdigit() else None

                        Libro.objects.create(
                            titulo=fila.get('titulo', '').strip(),
                            autor=fila.get('autor', '').strip(),
                            descripcion=fila.get('descripcion', '').strip(),
                            genero=fila.get('genero', 'otro').strip(),
                            anio_publicacion=anio,
                            isbn=fila.get('isbn', '').strip(),
                            disponible=disponible,
                        )
                        creados += 1
                    except Exception:
                        errores += 1

                messages.success(request, f'✅ Importación completada: {creados} libros añadidos.')
                if errores:
                    messages.warning(request, f'⚠️ {errores} filas no pudieron importarse.')
                return redirect('libro_list')

            except Exception as e:
                messages.error(request, f'❌ Error al leer el archivo: {e}')

    return render(request, 'biblioteca/csv_import.html', {'form': form})