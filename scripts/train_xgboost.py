import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Ruta del archivo de datos preprocesados
DATA_FILE = "../data/preprocessed/metrics_preprocessed.csv"

# Función para entrenar el modelo XGBoost


def train_xgboot():
    # Cargar los datos preprocesados
    df = pd.read_csv(DATA_FILE)

    # Separar características (X) y etiquetas (y)
    X = df.drop(columns=["pod", "cpu_usage_label", "memory_usage_label",
                "network_in_label", "network_out_label"])
    y = df[["cpu_usage_label", "memory_usage_label",
            "network_in_label", "network_out_label"]]

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Crear el modelo XGBoost
    model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")

    # Entrenar el modelo para cada una de las métricas etiquetadas
    models = {}
    for label in y.columns:
        print(f"Entrenando modelo para: {label}...")
        model.fit(X_train, y_train[label])
        models[label] = model

        # Realizar predicciones y evaluar la precisión
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test[label], y_pred)
        print(f"Precisión para {label}: {accuracy * 100:.2f}%")

    # Guardar los modelos entrenados
    for metric, model in models.items():
        model.save_model(f"../models/xgboost_model_{metric}.json")
        print(f"Modelo para {metric} guardado")


if __name__ == "__main__":
    train_xgboot()
