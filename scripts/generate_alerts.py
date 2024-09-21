import pandas as pd
from xgboost import XGBClassifier

# Ruta del archivo de datos preprocesados
DATA_FILE = "../data/preprocessed/metrics_preprocessed.csv"

# Función para cargar los modelos entrenados


def load_models():
    models = {}
    metrics = ["cpu_usage_label", "memory_usage_label",
               "network_in_label", "network_out_label"]

    for metric in metrics:
        model = XGBClassifier()
        model.load_model(f"../models/xgboost_model_{metric}.json")
        models[metric] = model

    return models

# Función para generar alertas basadas en las predicciones del modelo


def generate_alerts():
    # Cargar los datos preprocessados
    df = pd.read_csv(DATA_FILE)

    # Cargar los modelos entrenados
    models = load_models()

    # Separar las características (X)
    X = df.drop(columns=["pod", "cpu_usage_label",
                "memory_usage_label", "network_in_label", "network_out_label"])

    # Generar predicciones para cada métrica
    alerts = {}
    for metric, model in models.items():
        y_pred = model.predict(X)
        alerts[metric] = y_pred

    # Imprimir alertas
    for metric, preds in alerts.items():
        print(f"Alertas para {metric}: {preds}")


if __name__ == "__main__":
    generate_alerts()
