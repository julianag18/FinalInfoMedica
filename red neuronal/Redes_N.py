import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

# Cargar datos
archivo = "C:/Users/vcamaclo/Downloads/dabe de datos.xlsx/datos_modelo_GRD.xlsx"
df = pd.read_excel(archivo)

# Codificar variables categóricas
categoricas = ['Sexo', 'Tipo de ingreso', 'Dx principal de egreso', 'Infecciones', 'Situacion al alta', 'Tipo servicio']
for col in categoricas:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))

X = df[['Edad', 'Sexo', 'Tipo de ingreso', 'Dx principal de egreso', 'Duración estancia',
        'Días de Unidad Cuidado Intensivo', 'Infecciones', 'Situacion al alta',
        'Num_Procedimientos', 'Tipo servicio']]

# Imputar valores faltantes
imputer = SimpleImputer(strategy='median')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Variable objetivo: agrupar GRDs poco frecuentes en "OTRO"
y = df['GRD -Código'].astype(str)
grd_counts = y.value_counts()
max_count = grd_counts.max()
umbral = max_count * 0.20  # 20% del máximo
top_grds = grd_counts[grd_counts >= umbral].index
y = y.where(y.isin(top_grds), 'OTRO')

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Entrenar modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Reporte de desempeño
print(classification_report(y_test, y_pred))