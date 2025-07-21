import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, label_binarize
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# 1️⃣ Cargar datos
df = pd.read_excel("C:/Users/storo/Downloads/datos_limpios.xlsx")

# 2️⃣ Imputación de valores nulos
df.fillna(df.mean(numeric_only=True), inplace=True)
df.fillna('Desconocido', inplace=True)

# 3️⃣ Definir variables predictoras (basadas en las columnas conservadas)
features = [
    'Edad',
    'Sexo', 'Tipo de ingreso',
    'Días estancia', 'ServicioAlta', 'Días de Unidad Cuidado Intensivo', 'Dx principal de egreso',
    'Dxr 1', 'Dxr 2', 'Dxr 3', 'Dxr 4', 'Dxr 5', 'Dxr-6', 'Dxr 7', 'Dxr 8', 'Dxr 9',
    'Código causa externa', 'Situacion al alta',
    'Proc1', 'Proc2', 'Proc3', 'Proc4', 'Proc5', 'Proc6',
    'Proc7', 'Proc8', 'Proc9', 'Proc10', 'Proc11', 'Proc12',
    'Tipo servicio', 'Infecciones'
]

X = pd.get_dummies(df[features])

# 4️⃣ Preparar etiquetas (GRD - Código)
y_raw = df['GRD -Código'].astype(str)

# Filtrar GRDs frecuentes (≥ 20% del GRD más frecuente)
grd_counts = y_raw.value_counts()
umbral = grd_counts.max() * 0.20
grds_frec = grd_counts[grd_counts >= umbral].index
y_filtered = y_raw.where(y_raw.isin(grds_frec), 'OTRO')

# Codificar etiquetas
le = LabelEncoder()
y_encoded = le.fit_transform(y_filtered)

# Eliminar clases con solo 1 muestra
mask = [Counter(y_encoded)[label] > 1 for label in y_encoded]
X = X[mask]
y_encoded = y_encoded[mask]

# 5️⃣ Dividir conjunto de datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
)

# 6️⃣ Escalado
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 7️⃣ Definir modelo
mlp = MLPClassifier(hidden_layer_sizes=(128, 64, 32),
                    activation='relu',
                    solver='adam',
                    alpha=0.001,
                    batch_size=32,
                    learning_rate='adaptive',
                    max_iter=100,
                    early_stopping=True,
                    validation_fraction=0.1,
                    n_iter_no_change=10,
                    random_state=42,
                    verbose=True)

# 8️⃣ Entrenar modelo
mlp.fit(X_train, y_train)

# 9️⃣ Evaluación
y_pred = mlp.predict(X_test)
y_pred_proba = mlp.predict_proba(X_test)

print("\n📋 Reporte de clasificación:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# 🔄 Exportar a archivos para Django
import joblib
import json

# Guardar modelo MLP entrenado
joblib.dump(mlp, 'modelo_grd.pkl')

# Guardar scaler
joblib.dump(scaler, 'scaler.pkl')

# Guardar label encoder (para decodificar el resultado en Django)
joblib.dump(le, 'labelencoder.pkl')

# Guardar columnas del dataframe dummificado (para asegurar consistencia al predecir)
with open('columnas_modelo.json', 'w') as f:
    json.dump(X.columns.tolist(), f)

print("\n✅ Archivos guardados: modelo_grd.pkl, scaler.pkl, labelencoder.pkl, columnas_modelo.json")
