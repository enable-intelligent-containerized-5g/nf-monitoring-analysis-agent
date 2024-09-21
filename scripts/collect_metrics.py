import requests
import yaml
import json
import pandas as pd
import time
from datetime import datetime
import signal
import sys

# Rutas de configuración
PROMETHEUS_URL = "http://localhost:30090/api/v1/query"
QUERIES_FILE = "../config/prometheus_queries.yml"
THRESHOLDS_FILE = "../config/thresholds.json"

# Variables globales
monitoring = True  # Controla si el monitoreo continúa

# Función para manejar la interrupción de teclado (Ctrl + C)


def signal_handler(sig, frame):
    global monitoring
    print("\nMonitoreo detenido manualmente.")
    monitoring = False

# Función para obtener datos de Prometheus


def get_prometheus_data(query):
    try:
        response = requests.get(PROMETHEUS_URL, params={'query': query})
        data = response.json()
        if 'data' in data and 'result' in data['data']:
            return data['data']['result']
    except Exception as e:
        print(f"Error al consultar Prometheus: {e}")
        return []

# Función para etiquetar las métricas según los umbrales definidos


def label_metrics(metric, thresholds):
    if metric < thresholds["normal"]:
        return "normal"
    elif metric < thresholds["alert"]:
        return "alert"
    else:
        return "critical"

# Cargar las consultas y umbrales desde archivos de configuración


def load_config():
    with open(QUERIES_FILE, 'r') as f:
        queries = yaml.safe_load(f)
    with open(THRESHOLDS_FILE, 'r') as f:
        thresholds = json.load(f)
    return queries, thresholds

# Función principal para recolectar y etiquetar métricas


def collect_metrics_and_label(queries, thresholds):
    labeled_data = {}

    # Recolectar todas las métricas por pod
    for metric_name, query in queries.items():
        results = get_prometheus_data(query)
        for result in results:
            pod = result["metric"]["pod"]
            value = float(result["value"][1])

            # Si es la primera vez que se encuentra este pod, inicializar su diccionario
            if pod not in labeled_data:
                labeled_data[pod] = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            # Guardar el valor de la métrica y su etiqueta
            labeled_data[pod][f"{metric_name}_value"] = value
            labeled_data[pod][f"{metric_name}_label"] = label_metrics(
                value, thresholds[metric_name])

    # Convertir los datos a un DataFrame
    df = pd.DataFrame.from_dict(labeled_data, orient="index")
    df.reset_index(inplace=True)
    df.rename(columns={"index": "pod"}, inplace=True)

    return df

# Función para ejecutar el monitoreo continuo


def start_monitoring(interval):
    queries, thresholds = load_config()
    start_time = datetime.now()  # Tiempo de inicio del monitoreo
    all_data = []

    global monitoring
    while monitoring:
        df = collect_metrics_and_label(queries, thresholds)
        all_data.append(df)

        # Esperar el intervalo de tiempo antes de la siguiente recolección
        time.sleep(interval)

    end_time = datetime.now()  # Tiempo de fin del monitoreo

    # Concatenar todos los DataFrames recolectados
    full_df = pd.concat(all_data)

    # Formato del archivo CSV con el rango de tiempo del monitoreo
    file_name = f"../data/labeled/metrics_labeled_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}_to_{end_time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    # Guardar el DataFrame completo en CSV
    full_df.to_csv(file_name, index=False)
    print(f"Métricas etiquetadas guardadas en: {file_name}")


# Ejecutar el script
if __name__ == "__main__":
    # Manejar la interrupción manual (Ctrl + C)
    signal.signal(signal.SIGINT, signal_handler)

    # Preguntar por el intervalo de monitoreo
    try:
        interval = float(
            input("Ingrese el intervalo de recolección de métricas (en segundos): "))
    except ValueError:
        print("Entrada inválida, se utilizará el intervalo predeterminado de 5 segundos.")
        interval = 5.0

    print(
        f"Iniciando monitoreo con un intervalo de {interval} segundos. Presiona Ctrl + C para detener.")

    # Iniciar el monitoreo continuo
    start_monitoring(interval)
