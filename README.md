# Proyecto MLOps de Steam
## Introducción
Bienvenido al proyecto MLOps de Steam! En este proyecto, asumiremos el rol de un Ingeniero MLOps en Steam, una plataforma de juegos multinacional. Nuestra misión es crear un sistema de recomendación de videojuegos utilizando aprendizaje automático. Los datos necesitan ser refinados, y nuestra tarea es transformarlos en un estado utilizable, desarrollar un Producto Mínimo Viable (MVP) y desplegarlo como una API RESTful.

## Descripción del Problema
Como Científico de Datos en Steam, nuestra tarea es crear un modelo de aprendizaje automático para un sistema de recomendación de videojuegos. El estado actual de los datos es crudo y no procesado, lo que dificulta el trabajo. Nuestro objetivo es empezar desde cero, realizar tareas rápidas de Ingeniería de Datos

## Información del Juego en Steam
En este proyecto, trabajamos con tres archivos JSON que contienen datos cruciales sobre los juegos en la plataforma Steam. Cada archivo aporta una perspectiva única:
* user_reviews.json.gz: <br>
Este conjunto de datos es como un caleidoscopio de opiniones de usuarios sobre los juegos que han experimentado en Steam. Ofrece detalles sobre si recomendaron o no un juego y estadísticas sobre la utilidad de los comentarios. Además, revela el ID del usuario, su URL de perfil y el ID del juego que están comentando.

* users_items.json.gz:<br>
Aquí, obtenemos una visión panorámica de los juegos que cada usuario ha jugado y cuánto tiempo les han dedicado.

* steam_games.json.gz: <br>
Este conjunto de datos proporciona una ventana a los propios juegos en Steam. Incluye información vital como títulos, desarrolladores, precios, características técnicas y etiquetas.

## Flujo de Trabajo Propuesto

### Ingeniería de Datos

- **Limpieza y Transformación de Datos:** Enfoque inicial en leer el conjunto de datos en el formato correcto. Eliminar columnas innecesarias para optimizar el rendimiento de la API y el entrenamiento del modelo. En este proyecto el etl se divide entre los tres conjuntos de datos que fueron proporcionados y ofrecen informacion acerca de las distintas caracteristicas y opiniones de los juegos presentes en la plataforma.
["ETL Output"](01_ETL_Output.ipynb)
["ETL Users Items"](01_ETL_user_items.ipynb)
["ETL Users Reviews"](01_ETL_user_reviews.ipynb)
