# ti2041-2024

Proyecto Django - Gestión de Productos S.A
Aplicación web constuida con Django en Python.

Requisitos técnicos:
    -Requisitos de software:
        Python: Versión 3.8 o superior.
        Django: Versión 3.x.x o superior.
        Pip: Administrador de paquetes.
        Base de datos: SQLite.

Lineas de comando:
    git clone https://github.com/yskaaren/ti2041-2024.git
    cd .\Evaluaciones\
    cd .\Sumativa_1\
    Ejecutar servidor de desarrollo: python manage.py runserver
    Acceder a la aplicación: http://127.0.0.1:8000/productos

Estructura del proyecto
    productos: Contiene la app encargada de la gestión de productos, con sus modelos, vistas y templates.
    templates: Contiene plantillas HTML para consultar, registrar y consultar productos.
    manage.py: Comando para ejecutar el servidor, migraciones, etc.
    db.sqlite3: Base de datos utilizada en el proyecto.


Usuario admin acceder al administrador de Django y visualizar los modelos creados:
    user: admin
    pass: 1234