from flask import Flask, render_template, send_file
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Unillanos"]
collection = db["Aspirantes"]

@app.route('/')
def mostrar_datos():
    # Traer todos los documentos de la colección
    datos = list(collection.find())
    # Convertir ObjectId a string para evitar errores en la plantilla
    for d in datos:
        d["_id"] = str(d["_id"])
    return render_template('mostrar.html', datos=datos)

@app.route('/grafico')
def grafico():
    # Obtener los datos desde MongoDB
    datos = list(collection.find())
    df = pd.DataFrame(datos)

    # Verificar que el campo PAIS exista
    if 'PAIS' not in df.columns:
        return "No se puede generar el gráfico: campo 'PAIS' no encontrado", 400

    # Agrupar por país
    conteo = df['PAIS'].value_counts()


    # Crear gráfico
    plt.figure(figsize=(10, 6))
    conteo.plot(kind='bar', color='mediumseagreen')
    plt.title('Cantidad de aspirantes por país')
    plt.xlabel('País')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar imagen en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

@app.route('/grafico2')
def grafico2():
    # Obtener los datos desde MongoDB
    datos = list(collection.find())
    if not datos:
        return "No hay datos en la colección", 400

    df = pd.DataFrame(datos)

    # Verificar que el campo GENERO exista
    if 'GENERO' not in df.columns:
        return "No se puede generar el gráfico: campo 'GENERO' no encontrado", 400

    # Contar la cantidad de admitidos según GENERO
    diagram = df['NATURALEZA_COLEGIO'].value_counts()

    # Crear gráfico de pastel
    plt.figure(figsize=(8, 8))
    diagram.plot(
        kind='pie',
        autopct='%1.1f%%',  # Muestra porcentaje
        startangle=90,  # Rotación inicial
        colors=['mediumseagreen', 'lightcoral'],  # Puedes personalizar colores
        explode=[0.05] * len(diagram)  # Separa ligeramente las porciones
    )
    plt.title('Distribución de aspirantes según Naturaleza de Colegio')
    plt.ylabel('')  # Ocultar etiqueta del eje Y
    plt.tight_layout()

    # Guardar imagen en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)