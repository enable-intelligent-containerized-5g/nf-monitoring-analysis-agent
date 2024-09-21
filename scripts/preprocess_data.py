import pandas as pd
import os

# Ruta donde se guardan los CSVs etiquetados
DATA_FOLDER = "../data/labeled/"

# Función para cargar y concatenar todos los archivos CSV de métricas etiquetadas


def load_data():
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    df_list = []

    for file in all_files:
        file_path = os.path.join(DATA_FOLDER, file)
        df = pd.read_csv(file_path)
        df_list.append(df)

    # Concatenar todos los archivos en un solo DataFrame
    full_df = pd.concat(df_list, ignore_index=True)
    return full_df

# Función para preprocesar los datos


def preprocess_data(df):
    # Eliminar columnas innecesarias (por ejemplo, la columna de timestamp)
    df = df.drop(columns=["timestamp"])

    # Convertir etiquetas categóricas (normal, alert, critical) en valores numéricos
    label_mapping = {"normal": 0, "alert": 1, "critical": 2}

    for column in df.columns:
        if "label" in column:
            df[column] = df[column].map(label_mapping)

    # Retornar el DataFrame preprocesado
    return df

# Función principal


def main():
    df = load_data()
    df_preprocessed = preprocess_data(df)

    # Guardar el DataFrame preprocesado en un archivo CSV
    output_file = "../data/preprocessed/metrics_preprocessed.csv"
    df_preprocessed.to_csv(output_file, index=False)
    print(f"Datos preprocesados guardados en: {output_file}")


if __name__ == "__main__":
    main()
