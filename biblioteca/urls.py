from django.urls import path
from . import views

urlpatterns = [
    path('', views.libro_list, name='libro_list'),
    path('libro/<int:pk>/', views.libro_detail, name='libro_detail'),
    path('libro/nuevo/', views.libro_create, name='libro_create'),
    path('libro/<int:pk>/editar/', views.libro_edit, name='libro_edit'),
    path('libro/<int:pk>/eliminar/', views.libro_delete, name='libro_delete'),
    path('csv/exportar/', views.export_csv, name='export_csv'),
    path('csv/importar/', views.import_csv, name='import_csv'),
]