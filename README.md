# FinalInfoMedica
Este repositorio contiene todo el código, datos y documentación necesarios para el desarrollo, entrenamiento y evaluación de un modelo de Redes Neuronales destinado a la predicción de Grupos Relacionados por el Diagnóstico (GRD).

1. Estructura de directorios red neuronal
red neuronal/                # Carpeta raíz del proyecto de red neuronal
│
├── redes_neuronales.ipynb    # Notebook principal: análisis estadístico y definición del modelo inicial
├── finalinformaticamedica.ipynb  # Notebook de ajustes finales: hiperparámetros, benchmarks y métricas
│
├── tests/                    # Notebooks de prueba y experimentación (ignorables en producción)
│   ├── juli.ipynb
│   ├── julianapruebas.ipynb
│   ├── pruebas.ipynb
│   └── pruebas_redes.ipynb
│
└── databases/                # Bases de datos usadas en el proyecto
    ├── dabe de datos.xlsx        # Base original sin procesar
    ├── datos_modelo_GRD.xlsx     # Resultado del análisis estadístico inicial y filtrado (entrada al modelo)
    └── datos_limpios.xlsx        # Subconjunto para pruebas de mejora de precisión en la red

2. Descripción de archivos y carpetas
2.1 red neuronal/
Carpeta principal que agrupa todo lo relacionado con la creación, ajuste y pruebas del modelo de redes neuronales.

- redes_neuronales.ipynb: Contiene el análisis exploratorio de datos (EDA) completo: limpieza, tratamiento de valores faltantes y selección de variables. Describe cómo se filtró la base original (dabe de datos.xlsx) para obtener datos_modelo_GRD.xlsx, conservando columnas con al menos 2% de datos no nulos. Incluye la definición de la arquitectura de la red neuronal usada en producción.

- finalinformaticamedica.ipynb: Versión extendida donde se ajustaron hiperparámetros y parámetros de entrenamiento (tasa de aprendizaje, número de capas y neuronas, funciones de activación, optimizadores). Reporta métricas de rendimiento (precisión global ≈ 80%, matriz de confusión, curvas ROC). Aquí es necesario aclarar que se automatizó el filtrado de la base virgen para mejorar eficiencia, y pero no se integró directamente en Django por limitaciones computacionales.

2.2 tests/
Contiene notebooks de experimentación que muestran el proceso de prueba y error con distintas variantes de modelos: juli.ipynb, julianapruebas.ipynb, pruebas.ipynb, pruebas_redes.ipynb. Cada uno explora cambios en hiperparámetros, arquitecturas alternativas o preprocesamientos puntuales. No son necesarios para la ejecución del modelo final, pero documentan el recorrido investigativo.

2.3 databases/
Repositorio de las diferentes versiones de la base de datos:

- dabe de datos.xlsx: Base de datos original, sin ningún filtrado.

- datos_modelo_GRD.xlsx: Generada tras el análisis estadístico y filtrado en informeEDA.ipynb. Entrada principal para el modelo inicial (redes_neuronales.ipynb).

- datos_limpios.xlsx: Conjunto reducido utilizado exclusivamente para pruebas de mejora de precisión en redes neuronales. Sirvió de validación interna antes de definir el modelo final.

3. Notebooks auxiliares
- informeEDA.ipynb (ubicado fuera de la carpeta red neuronal): Notebook con análisis estadístico detallado de las variables originales y descripción paso a paso del filtrado que llevó a datos_modelo_GRD.xlsx. Incluye visualizaciones y justificación de la retención/eliminación de columnas.

- redes_neuronales_.ipynb (también fuera de red neuronal): Versión anterior al ajuste final, usada en producción Django para predicción de GRD. Combina análisis estadístico y construcción del modelo, aunque sin la automatización ni los filtros probados de finalinformaticamedica.ipynb.

