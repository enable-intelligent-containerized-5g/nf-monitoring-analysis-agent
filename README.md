# Monitoreo de Red 5G UPF

Este proyecto implementa un sistema de monitoreo y alerta en tiempo real para las funciones de red UPF (User Plane Function) en una red 5G contenerizada en Kubernetes. Utiliza métricas recolectadas a través de Prometheus y un modelo de aprendizaje automático (XGBoost) para predecir condiciones críticas en los pods.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Uso](#uso)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Características

- Recolección de métricas en tiempo real de pods UPF.
- Análisis de métricas utilizando modelos de aprendizaje automático.
- Generación de alertas cuando se superan umbrales críticos.
- Interfaz de línea de comandos simple para la ejecución y monitoreo.

## Requisitos

- Python 3.7 o superior
- Bibliotecas de Python:
  - `pandas`
  - `numpy`
  - `xgboost`
  - `requests`
  - `tqdm` (opcional para la barra de progreso)

Puedes instalar las dependencias necesarias utilizando pip:

```bash
pip install pandas numpy xgboost requests tqdm
```

## Estructura del Proyecto

```
upf-monitoring/
│
├── config/
│   ├── prometheus_queries.yml
│   └── thresholds.json
│
├── data/
│   ├── labeled/
│   ├── preprocessed/
│   └── raw
│
├── logs/
│
├── modes/
│
├── scripts/
│   ├── collect_metrics.py
│   ├── generate_alerts.py
│   ├── preprocess_data.py
│   ├── real_time_monitoring.py
│   └── train_xgboost.py
│
└── README.md
```

- **config/**: Contiene archivos de configuración para los umbrales y modelos.
- **scripts/**: Contiene scripts para la recolección de métricas, entrenamiento del modelo y monitoreo en tiempo real.

## Configuración

1. **Configura los umbrales** en `config/thresholds.json`. Define los niveles de alerta y críticos para cada métrica.

```json
{
  "latency": {
    "warning": 50,
    "critical": 100
  },
  "throughput": {
    "warning": 100,
    "critical": 50
  },
  ...
}
```

2. **Entrena el modelo** utilizando el script `train_xgboost.py`. Este script utiliza los datos preprocesados en `data/preprocessed/` y guarda el modelo en `models/`.

```bash
python scripts/train_xgboost.py
```

## Uso

Para ejecutar el sistema de monitoreo en tiempo real utilizando el script `real_time_monitoring.py`.

```bash
python scripts/real_time_monitoring.py
```

Esto iniciará la recolección de métricas y la generación de alertas en tiempo real. Puedes detener el script con `Ctrl + C`.

## Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request.

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

### Notas:

- Puedes ajustar el contenido según sea necesario, especialmente las secciones de instalación y uso, para que se alineen mejor con tu proyecto.
- Asegúrate de incluir detalles sobre cómo entrenar el modelo si es necesario.
- Si tienes más scripts o archivos que quieras incluir, actualiza la estructura del proyecto en consecuencia.

Si necesitas cambios o más detalles en alguna sección, ¡házmelo saber!
