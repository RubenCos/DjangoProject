# DjangoProject

Aplicación desarrollada con Django para la gestión de una biblioteca.

## Requisitos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.10 o superior
- pip
- Git (opcional)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/RubenCos/DjangoProject.git
cd DjangoProject
```

### 2. Crear y activar el entorno virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

Crear las migraciones de la aplicación:

```bash
python manage.py makemigrations biblioteca
```

Aplicarlas a la base de datos:

```bash
python manage.py migrate
```

### 5. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en:

```text
http://127.0.0.1:8000/
```

## Estructura básica

```text
DjangoProject/
├── biblioteca/ 
├── web_project
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```
Es proyecto monolitico modular en el que en ```web_project``` continee la configuración global del proyecto y divide la lógica de negocio (vistas, modelos, urls...) en cada aplicación, como es en este caso ```biblioteca```

## Tecnologías utilizadas

- Python
- Django
- SQLite
- HTML
- CSS

## Autor

- GitHub: (https://github.com/RubenCos)