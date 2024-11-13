# Meli SAMM Challenge

### Descripción del Proyecto

Este proyecto es una solución ETL diseñada para monitorear el uso de la aplicación y el progreso de las tareas asociadas a proyectos en la aplicación Todoist. Utilizando un entorno de contenedores con Docker, se implementa una arquitectura que permite la extracción, transformación y carga (ETL) de datos hacia una base de datos PostgreSQL, simulando el consumo de datos de la API de Todoist. La información es posteriormente visualizada en Tableau.

### Simulación de Datos

Para este proyecto, la información se simula mediante la generación de datos aleatorios que emulan la estructura de los objetos `proyectos`, `tareas` y `actividades` de la API de Todoist. La generación de datos se realiza en el archivo `data_generation/random_data_generator.py`, utilizando la librería `Faker`
El objetivo de la simulación de datos es proporcionar un conjunto de datos realista que permita:
- Probar el proceso ETL para verificar la correcta carga y transformación de datos en PostgreSQL.
- Proveer datos suficientes para responder a las preguntas del challenge y generar visualizaciones en Tableau.
- Emular escenarios de uso de la aplicación Todoist, incluyendo el comportamiento de usuarios, estados de tareas y progreso de proyectos a lo largo del tiempo.

### Estructura del Proyecto

La estructura de carpetas es la siguiente:

A continuación se detalla la información de cada uno de los archivos:

- `data_generation/random_data_generator.py`: Genera los datos de prueba para replicar el comportamiento de los objetos proyectos, tareas y actividades de la API Todoist.
- `etl/config.json`: Configuración del proyecto para rutas de salida y otros parámetros.
- `etl/extraction.py`: Extrae los datos simulados y los guarda en formato JSON.
- `etl/load.py`: Carga los datos en PostgreSQL a partir del archivo JSON.
- `output_data/data.json`: Archivo de datos generado por `extraction.py`.
- `queries/postgres_queries.sql`: Contiene las consultas SQL que alimentan el tablero en Tableau para responder las preguntas del challenge.
- `.env`: Archivo de variables de entorno para almacenar configuraciones sensibles.
- `docker-compose.yml`: Configuración de Docker Compose para levantar los contenedores.
- `Dockerfile.etl`: Configura el contenedor para ejecutar el proceso ETL.
- `requirements.txt`: Dependencias de Python.




