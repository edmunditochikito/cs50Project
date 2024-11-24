# Sistema para Agendar Citas en Línea en un Restaurante
**Título:** Sistema para Agendar Citas en Línea en un Restaurante  
**Autor:** Edmundo Ariel Aguilar Alfaro, Adrián de Jesús Sánchez González  
**Ubicación:** Nicaragua, Managua  
**Video de Presentación:** Inserta el enlace aquí

## Descripción
ReservaYa es una aplicación web diseñada para que los clientes puedan realizar reservaciones en restaurantes de manera rápida y sencilla. Proporciona una interfaz amigable que permite a los usuarios seleccionar mesas disponibles, ingresar información relevante y recibir confirmación.

### Características Principales:
- Registro e inicio de sesión utilizando autenticación y autorización con JWT (JsonWebToken).
- Opciones administrativas para el registro, edición y eliminación de platillos.
- Opciones administrativas para el registro, edición y eliminación de mesas.
- Exportación de datos en formato Excel o CSV.
- Impresión de tablas en formato PDF.
- Almacenamiento y eliminación de imágenes de platillos en la base de datos.
- Pantallas con diseño responsive.

### Tecnologías Utilizadas:
- Python
- Flask
- JavaScript
- HTML
- CSS
- SQLAlchemy
- MySQL
- Bootstrap
- JWT
- SweetAlert2
- Axios
- Flask-SQLAlchemy
- Flask-JWT-Extended
- PyMySQL

### Instrucciones para Ejecutar:
1. descargar el codigo fuente
2. instalar la carpeta de requirements.txt usando el comando pip install -r requirements.txt
3. crear un archivo llamado .env y agregar las siguientes variables de entorno
4. SECRET_KEY=la informacion que quieras para generar la llave secreta de la aplicacion
5. JWT_SECRET_KEY=la informacion que quieras para generar la llave secreta con la que firmar el token de acceso
6. crear la base de datos usando el script .sql 
7. cambiar el archivo config para hacer referencia a la nueva base de datos
8. en el archivo config puedes cambiar las llaves secretas antes mencionadas en caso de no querere usar archivos de entorno