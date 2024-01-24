# Proyecto MLOps de Steam
![Static Badge](https://img.shields.io/badge/Python-gray?style=flat&logo=python)
![Static Badge](https://img.shields.io/badge/-Pandas-gray?style=flat&logo=pandas)
![Static Badge](https://img.shields.io/badge/Numpy-gray?style=flat&logo=Numpy)
![Static Badge](https://img.shields.io/badge/FastApi-darkseagreen)
![Static Badge]("https://img.shields.io/badge/Render-cyan")

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
["ETL Steam_Games"](./Notebooks/ETL_steam_games.ipynb) 
["ETL Users Items"](./Notebooks/ETL_user_items.ipynb)
["ETL Users Reviews"](./Notebooks/ETL_user_reviews.ipynb)

- **Análisis de Sentimiento:** Crear una nueva columna, 'sentiment_analysis', aplicando análisis de sentimiento mediante Procesamiento de Lenguaje Natural (NLP) a las reseñas de usuarios. La escala que se utilizo fue: '0' para comentarios negativos, '1' para neutrales y '2' para positivos.

### Análisis Exploratorio de Datos (EDA)

- **Exploración Manual:** Realizar un EDA manual después del ETL para investigar las relaciones entre variables, identificar valores atípicos y descubrir patrones interesantes dentro del conjunto de datos, para esta tarea se utilizan diferentes librerias para hacer visualizaciones y medidas estadisticas. ["EDA"](./Notebooks/EDA.ipynb)

- **Creación de DataFrames Auxiliares:** Antes de desarrollar las funciones de la API, se crearon DataFrames auxiliares para optimizar el espacio y mejorar el rendimiento de las funciones. Estos DataFrames se utilizaron para almacenar datos específicos necesarios para las consultas de la API. ["Dataframes Auxiliares](./DataFrames_Auxiliare.ipynb)

### Desarrollo de la API

- **Framework:** Utilizar el framework FastAPI para exponer los datos de la empresa a través de endpoints RESTful.
- **Endpoints:**
  - `PlayTimeGenre(genero: str)`: Devuelve el año de lanzamiento con más horas jugadas para el género especificado.
  - `UserForGenre(genero: str)`: Devuelve el usuario con más horas jugadas para el género dado y una lista de acumulación de horas jugadas por año.
  - `UsersRecommend(año: int)`: Devuelve el top 3 de juegos más recomendados por usuarios para el año especificado.
  - `UsersWorstDeveloper(año: int)`: Devuelve el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año especificado.
  - `sentiment_analysis(empresa_desarrolladora: str)`: Devuelve un diccionario con el recuento de análisis de sentimiento para reseñas asociadas con el desarrollador de juegos especificado.

  - Dentro de la carpeta Datasets se encuentran los dataframes utilizados para cada funcion y en este archivo se probaron la funciones antes de utilizar FastAPI ["Funciones API"](./Funciones_API.ipynb)

### Modelo de Aprendizaje Automático

En esta fase del proyecto, se llevó a cabo el modelado para el desarrollo del Sistema de Recomendación, basado en la similitud del coseno, donde se crearon las siguientes funciones:

Primera Función item-item, introduzco el id del juego y me devuelve juegos recomendados.

Segunda Función de usuario-item, Ingreso el id del usuario y le devuelve juegos recomendados.

Para el primer enfoque del modelo, se establece una relación ítem-ítem. En este escenario, se evalúa un ítem con respecto a su similitud con otros ítems para ofrecer recomendaciones similares. En este caso, el input corresponde a un juego y el output es una lista de juegos recomendados, utilizando el concepto de similitud del coseno.

Por otra parte, se considera una segunda propuesta para el sistema de recomendación, basada en el filtro user-item. En esta estrategia, se analiza a un usuario para identificar usuarios con gustos similares y se recomiendan ítems que hayan sido apreciados por estos usuarios afines.

Acá el trabajo realizado: ["Modelo"](./Modelo_Recomendacion.ipynb)

## FastAPI

Si desea ejecutar la API desde el localhost debe seguir los siguientes pasos: 

- Clonar el proyecto haciendo git clone **git@github.com:/DomiAndi/PI_MLOps_Steam**

- Preparación del entorno de trabajo en **Visual Studio Code**

* Crear entorno **python -m venv** entorno (o el nombre que usted desee)

* Ingresar al entorno haciendo **entorno\bin\activate**, en el caso si usa Windows entorno\Scripts\activate

- Instalar dependencias con **pip install -r requirements.txt**

- Ejecutar el archivo **main.py** desde consola activando uvicorn. Si usted importa la libreria uvicorn en el archivo **main.py**, desde la consola escribir **python main.py** y correra facilmente. De lo contrario puedes hacer **uvicorn main:app --reload**

- Hacer Ctrl + clic sobre la dirección **http://XXX.X.X.X:XXXX**  (eso se visualizara en su Terminal).

- Una vez en el navegador, **agregar /docs para acceder**.

- En cada una de las funciones hacer clic en **Try it out** y luego introducir el dato que requiera o utilizar los ejemplos por defecto. 

- Finalmente Ejecutar y observar la respuesta.

## Conclusión

Este proyecto integral de MLOps tiene como objetivo transformar datos de juegos en bruto en un sistema funcional de recomendación desplegado como una API. La optimización del espacio mediante DataFrames auxiliares es una estrategia clave para mejorar el rendimiento de las funciones al igual que utilizar el muestreo en el modelo de recomendacion. Al abordar la ingeniería de datos, la ingeniería de características, el desarrollo de la API, el EDA y el aprendizaje automático, buscamos proporcionar información valiosa y recomendaciones a los usuarios de Steam acerca de los juegos presentes en la plataforma.
