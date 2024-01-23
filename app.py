import pandas as pd
import numpy as np
import os

print("Nombre de la cuenca: ")
nombre = input()
print("\nIniciando el programa")

# Especifica la ruta de la carpeta que contiene los archivos CSV
carpeta = 'data/'

# Obtiene la lista de archivos en la carpeta
archivos_csv = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.csv')]

# Inicializa una lista para almacenar los dataframes
lista_dataframes = []

# Lee cada archivo CSV y agrega el dataframe a la lista
for archivo in archivos_csv:
    ruta_completa = os.path.join(carpeta, archivo)
    df = pd.read_csv(ruta_completa, sep = " ", header = None, names=["year","month","day","pp","max_temp","min_temp"])
    df.loc[df["pp"] < 0, "pp"] = np.nan # clean the data with Na
    df = df.groupby(['year', 'month'])['pp'].sum().reset_index()

    # Pivotar la tabla para tener meses como columnas
    df = df.pivot_table(index='year', columns='month', values='pp', aggfunc=np.sum)

    # Rename the columns
    df.columns = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    # Reemplazar NaN con -0.01
    df = df.fillna(-0.01)

    # Multiplicar por 100 y convertir a enteros (excepto la columna del año)
    df = (df * 100).astype(int).astype(str)

    # Eliminar el decimal para los valores enteros
    df = df.applymap(lambda x: x.rstrip('.0') if '.' in x else x)
    lista_dataframes.append(df)

print("Datos importados")
def handle_data(data, iteration, text):
    texto = text
    h, w = data.shape
    years = data.index.array
    for row in range(h):
        texto = texto + "H10"+ str(iteration) + str(years[row])
        for col in range(w):
            max_value = data.iloc[:,col].astype(int).max()
            value = len(str(max_value))
            space = "  "
            n = str(data.iloc[row,col])
            if len(n) == 2:
                space = space * value
            elif len(n) == 1:
                space = space * value
                space = space + " "
            elif value > len(n):
                resto = value - len(n)
                space = "  " * resto
                space = "  " + space
            texto = texto + space + str(n)
        texto = texto + "\n"
    return texto
print("Función creada.")

texto = "A                PRECIPITACION (MM)\nA                CUENCA: "
texto = texto + nombre +" (Formato para extender datos)\nA\nB       "
texto = texto + str(lista_dataframes[0].index.array[0])
texto = texto + "            1            1       "
texto = texto + str(len(lista_dataframes[0].index.array))
texto = texto + "           0           0            1           0           0           0\nC\n"

i = 1
for data in lista_dataframes:
    texto = handle_data(data, i, texto)
    i = i + 1
    percentage = round(((i - 1) / len(lista_dataframes)) * 100)
    print("["+str(percentage)+"%] completado.")

texto = texto + "A"

with open('DATOS.DAT', 'w') as f:
    f.write(texto)
print("Completado, archivo creado como DATOS.DAT")
