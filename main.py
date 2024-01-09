import pandas as pd
import numpy as np
import pyarrow as pa 
import pyarrow.parquet as pq 
from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.get('/')
def message():
    return "Api de consultas de videojuegos de la plataforma Steam. Instrucciones. Escriba /docs a continuacion de la URL actual de esta pagina para interactuar con la API "

#Importamos los datos que se encuentran en formato parquet para dataframes

df_PlayTimeGenre = pd.read_parquet("Datasets\df_PlayTimeGenre_hour_final1.parquet")
df_UserForGenre = pd.read_parquet("Datasets\df_UsersForGenre2_final.parquet")
df_UsersRecommend = pd.read_parquet("Datasets\df_UsersRecommend2_final.parquet")
df_UsersWorstDeveloper = pd.read_parquet("Datasets\df_UserWorstDeveloper_final1.parquet")
df_Sentiment_Analysis = pd.read_parquet("Datasets\df_Sentiment_analysis_final.parquet")
modelo_final= pd.read_csv('Datasets\modelo_reco_final.csv',low_memory=False)

#Primera funcion: PlaytimeGenre

@app.get("/PlayTimeGenre")
def PlayTimeGenre(genero:str):
    """
    La funcion devuelve el año con mas horas jugadas para dicho género.
    """
    generos = df_PlayTimeGenre[df_PlayTimeGenre["main_genre"]== genero] #Filtramos en el dataframe el genero que fue solicitado
    if generos.empty:  #Con esta linea nos aseguramos que si para ese genero no hay resultado se notifique
        return f"No se encontraron datos para el género {genero}"
    año_max = generos.loc[generos["playtime_hour"].idxmax()] #Primero identificamos la fila (indice) que tiene la máxima cantidad de horas jugadas para el género dado y posteriormente se selecciona esa fila a partir del indice
    result = {
        'Genero': genero,
        'Año con Más Horas Jugadas': int(año_max["release_year"]),
        'Total de Horas Jugadas': año_max["playtime_hour"]
    }

    return result

#Segunda funcion: UserForGenre

@app.get("/UserForGenre")
def UserForGenre(genero: str):
    """
    La funcion devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
    """
    generos2 = df_UserForGenre[df_UserForGenre["main_genre"]== genero]
    user_max = generos2.loc[generos2["playtime_hour"].idxmax()]["user_id"]
    horas_x_año = generos2.groupby(["release_year"])["playtime_hour"].sum().reset_index()
    horas_lista = horas_x_año.rename(columns={"release_year": "Año", "playtime_hour": "Horas"}).to_dict(orient="records")    
    result2 = {
        "Genero": genero,
        "Usuario con Más Horas Jugadas": user_max,
        "Total de Horas Jugadas Por Año": horas_lista
    }
    return result2

#Tercera funcion: UsersRecommend

@app.get("/UsersRecommend")
def UsersRecommend(anio:int):
    """
    Funcion que devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
    """
    df_año= df_UsersRecommend[df_UsersRecommend["year_posted"]== anio]
    if type(anio) != int:
        return {"Debes colocar el año en entero, Ejemplo:2012"}
    if anio < df_UsersRecommend["year_posted"].min() or anio > df_UsersRecommend["year_posted"].max():
        return {"Año no encontrado"}
    df_ordenado_recomendacion = df_año.sort_values(by="recommendation_count", ascending=False)
    top_3_juegos = df_ordenado_recomendacion.head(3)[["app_name","recommendation_count"]]
    result3 ={
        "Año": anio,
        "Top 3 Juegos Más Recomendados": top_3_juegos.to_dict(orient="records")
    }
    return result3

#Cuarta funcion: UsersWorstDeveloper

@app.get("/UsersWorstDeveloper")
def UsersWorstDeveloper(anio:int):
    """
    Funcion que devuelve el top 3 de desarrolladoras con juegos MENOS 
    recomendados por usuarios para el año dado.
    """
    df_año2 = df_UsersWorstDeveloper[df_UsersWorstDeveloper["year_posted"]== anio]
    if type(anio) != int:
        return {"Debes colocar el año en entero, Ejemplo:2012"}
    if anio < df_UsersRecommend["year_posted"].min() or anio > df_UsersRecommend["year_posted"].max():
        return {"Año no encontrado "}
    df_ordenado_recomendacion2 = df_año2.sort_values(by="recommendation_count", ascending=False)
    top_3_developers = df_ordenado_recomendacion2.head(3)[["developer","recommendation_count"]]
    result4 = {
        'Año': anio,
        'Top 3 Desarrolladoras Menos Recomendadas': top_3_developers.rename(columns={"developer": "Desarrolladora", "recommendation_count": "Conteo Recomendacion"}).to_dict(orient="records")
    }
    return result4

#Quinta funcion : sentiment_analysis

@app.get("/SentimentAnalysis")
def sentiment_analysis( desarrolladora : str ):
    """
    Funcion que devuelve un diccionario con el nombre de la desarrolladora como llave y una lista 
    con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con 
    un análisis de sentimiento como valor.
    """
    if type(desarrolladora) != str:
        return "Debes colocar un developer de tipo str, EJ:'07th Expansion'"
    if len(desarrolladora) == 0:
        return "Debes colocar un developer en tipo String"
    df_developer = df_Sentiment_Analysis[df_Sentiment_Analysis["developer"]== desarrolladora]
    sentiment_counts = df_developer.groupby("sentiment_analysis")["sentiment_analysis_count"].sum().to_dict()
    sentiment_dicc = {0: "Negativo", 1: "Neutral", 2: "Positivo"}
    sentiment_counts = {sentiment_dicc[key]: value for key, value in sentiment_counts.items()}
    result50 = {desarrolladora: sentiment_counts}
    return result50

#Sexta Función Sistema de recomendación Item-Item

@app.get("/juegos_item_item/{item_id}")

def juegos_poritem(item_id: int):
    juego = modelo_final[modelo_final['item_id'] == item_id]

    if juego.empty:
        return {"mensaje": f"El juego '{item_id}' no posee nada."}

    userX = juego.index[0]

    df_sample = modelo_final.sample(n=33, random_state=42)

    juego_input = [juego.iloc[0, 3:]]  # Características del juego de entrada

    sim_scores = cosine_similarity(juego_input, df_sample.iloc[:, 3:])

    sim_scores = sim_scores[0]

    juegos_similares = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != userX]
    juegos_similares = sorted(juegos_similares, key=lambda x: x[1], reverse=True)

    juegos_simi_indices = [i[0] for i in juegos_similares[:5]]
    nombres_juegossimi = df_sample.loc[juegos_simi_indices, 'app_name'].tolist()

    return {"juegos_similares": nombres_juegossimi}

# Septima Función Sistema de recomendación Usuario-Item

@app.get("/juegos_usuario_item/{user_id}")

def recomendacion_usuario(user_id: str):
    # Encuentra con el user_id los juegos recomendados
    if user_id in modelo_final['user_id'].values:
        juegos = modelo_final.index[modelo_final['user_id'] == user_id].tolist()[0]
        
        juego_caracteristicas = modelo_final.iloc[juegos, 3:].values.reshape(1, -1)
        
        render_similitud = cosine_similarity(modelo_final.iloc[:, 3:], juego_caracteristicas)
        juegos_similaresrecomend = render_similitud.argsort(axis=0)[::-1][1:6]
        juegos_similaresrecomend = juegos_similaresrecomend.flatten()[1:]
        juegos_similares = modelo_final.iloc[juegos_similaresrecomend]['app_name']
        
        return juegos_similares  
    else:
        return "El juego con el user_id especificado no existe en la base de datos."

# Ejecutar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)