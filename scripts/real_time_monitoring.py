import pandas as pd
import time
import json
from xgboost import XGBClassifier
from prometheus_api_client import PrometheusConnect
import yaml

# Cargar las consultas de Prometheus desde el archivo de configuración


def load_prometheus_queries():
    with open('../config/prometheus_queries.yml', 'r') as file:
        queries = yaml.safe_load(file)
    return queries

# Cargar los umbrales desde el archivo JSON


def load_thresholds():
    with open('../config/thresholds.json', 'r') as file:
        thresholds = json.load(file)
    return thresholds


# Configuración de Prometheus
# Cambia esto por la IP de tu Prometheus
PROMETHEUS_URL = "http://localhost:30090"
prometheus = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)

# Cargar los modelos entrenados


def load_models():
    models = {}
    metrics = ["cpu_usage_label", "memory_usage_label",
               "network_in_label", "network_out_label"]

    for metric in metrics:
        model = XGBClassifier()
        model.load_model(f"../models/xgboost_model_{metric}.json")
        models[metric] = model

    return models

# Obtener métricas de Prometheus


def get_metrics(queries):
    metrics_data = {}
    for metric, query in queries.items():
        result = prometheus.custom_query(query)
        metrics_data[metric] = {item['metric']['pod']
            : float(item['value'][1]) for item in result}
    return metrics_data

# Función para predecir y generar alertas


def predict_and_alert(metrics, models, thresholds):
    alerts = {}
    for pod, pod_metrics in metrics.items():
        # Prepara las características para la predicción
        X = pd.DataFrame([pod_metrics])

        # Realiza la predicción
        predictions = {metric: model.predict(
            X)[0] for metric, model in models.items()}

        for metric, pred in predictions.items():
            if pred == 1:  # Si la predicción es "alert"
                alerts[pod] = f"Alerta: {metric} en {pod} - Estado: Alert"
            elif pred == 2:  # Si la predicción es "critical"
                alerts[pod] = f"Alerta: {metric} en {pod} - Estado: Critical"

    # Generar alertas basadas en los umbrales
    for pod, pod_metrics in metrics.items():
        for metric, value in pod_metrics.items():
            if value >= thresholds[metric]['critical']:
                alerts[pod] = f"Alerta Crítica: {metric} en {pod} - Valor: {value}"
            elif value >= thresholds[metric]['alert']:
                alerts[pod] = f"Alerta: {metric} en {pod} - Valor: {value}"

    return alerts

# Función principal para monitoreo continuo


def main():
    queries = load_prometheus_queries()
    thresholds = load_thresholds()
    models = load_models()

    while True:
        # Obtener métricas
        metrics = get_metrics(queries)

        # Convertir las métricas a un formato adecuado
        metrics_flat = {}
        for pod in set(metrics["cpu_usage"].keys()).union(
                metrics["memory_usage"].keys(),
                metrics["network_in"].keys(),
                metrics["network_out"].keys(
                )):

            metrics_flat[pod] = {
                "cpu_usage_value": metrics["cpu_usage"].get(pod, 0),
                "memory_usage_value": metrics["memory_usage"].get(pod, 0),
                "network_in_value": metrics["network_in"].get(pod, 0),
                "network_out_value": metrics["network_out"].get(pod, 0),
            }

        # Generar alertas
        alerts = predict_and_alert(metrics_flat, models, thresholds)

        # Imprimir alertas
        for pod, alert in alerts.items():
            print(alert)

        # Esperar un intervalo antes de la próxima recolección
        time.sleep(10)  # Puedes ajustar este intervalo


if __name__ == "__main__":
    main()
