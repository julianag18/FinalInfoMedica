import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de gráficos
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 📂 2. Cargar los datos
df = pd.read_excel("dabe de datos.xlsx")  # Cambia si el nombre del archivo es distinto

# ✨ 3. Limpieza de nombres de columnas
df.columns = df.columns.str.strip().str.replace('\xa0', ' ').str.replace(' +', ' ', regex=True)

# 🔄 4. Homologación de variables

## Tipo de ingreso
df['Tipo de ingreso'] = df['Tipo de ingreso'].str.strip().str.upper()
df['Tipo de ingreso'] = df['Tipo de ingreso'].replace({
    'URGENCIAS': 'URGENCIA'
})

## Situacion al alta
df['Situacion al alta'] = df['Situacion al alta'].str.strip().str.upper()
df['Situacion al alta'] = df['Situacion al alta'].replace({
    'ALTA MÉDICA': 'ALTA MEDICA',
    'MUERTO': 'FALLECIDO'
})

## Tipo servicio
df['Tipo servicio'] = df['Tipo servicio'].str.strip().str.upper()
df['Tipo servicio'] = df['Tipo servicio'].replace({
    'CIRUGÍA': 'CIRUGIA',
    'N/A': 'NO APLICA',
    'N0 APLICA': 'NO APLICA',
    'U. ADULTOS': 'URGENCIA ADULTOS',
    'URGENCIA - ADULTOS': 'URGENCIA ADULTOS',
    'URGENCIA ADULTO': 'URGENCIA ADULTOS',
    'URGENCIA ADULTOS.': 'URGENCIA ADULTOS',
    'URGENCIA PEDÍATRICAS': 'URGENCIA PEDIATRICAS'
})

#Sexo
df['Sexo'] = df['Sexo'].str.strip().str.upper()
df['Sexo'] = df['Sexo'].replace({
    'F': 'F',
    'M': 'M'
})

#Infecciones
df['Infecciones'] = df['Infecciones'].str.strip().str.upper()
df['Infecciones'] = df['Infecciones'].replace({
    'no': 'NO',
    'si': 'SI',
})

#Infección Quirurgica
df['Infección Quirurgica'] = df['Infección Quirurgica'].str.strip().str.upper()
df['Infección Quirurgica'] = df['Infección Quirurgica'].replace({
    'no': 'NO',
    'si': 'SI',
})

# Tipo GRD
df['Tipo GRD'] = df['Tipo GRD'].str.strip().str.upper()
df['Tipo GRD'] = df['Tipo GRD'].replace({
    'q': 'Q',
    'm': 'M',
})

# 🧐 5. Revisión inicial
print("Tamaño del dataset:", df.shape)
print("\nTipos de datos:\n", df.dtypes)
print("\nPrimeras filas:\n", df.head())

# ❌ 6. Duplicados y valores nulos
print("\nDuplicados:", df.duplicated().sum())
print("\nValores nulos por columna:\n", df.isnull().sum())

# 📊 7. Análisis univariado

## 7.1 Variables numéricas
num_cols = ['Edad', 'Días estancia', 'Días de Unidad Cuidado Intensivo']

for col in num_cols:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print(df[col].describe())
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribución de {col}")
        plt.show()

## 7.2 Variables categóricas
cat_cols = ['Sexo', 'Tipo de ingreso', 'ServicioAlta', 'Situacion al alta', 'Infecciones', 'Tipo servicio']

for col in cat_cols:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print(df[col].value_counts())
        sns.countplot(data=df, x=col, order=df[col].value_counts().index)
        plt.title(f"Distribución de {col}")
        plt.xticks(rotation=45)
        plt.show()

# 🧮 8. Ingeniería de características

## Fechas
df['Fecha de ingreso'] = pd.to_datetime(df['Fecha de ingreso'], format='%d%m%Y', errors='coerce')
df['Fecha de egreso'] = pd.to_datetime(df['Fecha de egreso'], format='%d%m%Y', errors='coerce')
df['Duración estancia'] = (df['Fecha de egreso'] - df['Fecha de ingreso']).dt.days

## Número de procedimientos
proc_cols = [col for col in df.columns if 'Proc' in col]
df['Num_Procedimientos'] = df[proc_cols].notna().sum(axis=1)

# 📈 9. Análisis bivariado

## Edad vs Tipo GRD
if 'Tipo GRD' in df.columns:
    sns.boxplot(data=df, x='Tipo GRD', y='Edad')
    plt.title("Edad por Tipo GRD")
    plt.show()

## Dx principal de egreso vs Tipo GRD (top 10)
if 'Dx principal de egreso' in df.columns and 'Tipo GRD' in df.columns:
    top_dxs = df['Dx principal de egreso'].value_counts().head(10).index
    sns.countplot(data=df[df['Dx principal de egreso'].isin(top_dxs)],
                  x='Dx principal de egreso', hue='Tipo GRD')
    plt.title("Dx principal de egreso más comunes por Tipo GRD")
    plt.xticks(rotation=45)
    plt.show()

# 🔍 10. Correlación numérica
corr_vars = [col for col in ['Edad', 'Días estancia', 'Días de Unidad Cuidado Intensivo', 'Duración estancia', 'Num_Procedimientos'] if col in df.columns]
correlation = df[corr_vars].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title("Matriz de correlación entre variables numéricas")
plt.show()

# ✅ 11. Variables sugeridas para el modelo
features = ['Edad', 'Sexo', 'Tipo de ingreso', 'Dx principal de egreso', 'Duración estancia',
            'Días de Unidad Cuidado Intensivo', 'Infecciones', 'Situacion al alta',
            'Num_Procedimientos', 'Tipo servicio']

features = [f for f in features if f in df.columns]

print("\n🔮 Variables sugeridas como input del modelo:")
print(features)


# Definir la variable objetivo
target = 'GRD -Código'

# Asegurarse de que esté en el DataFrame y agregarla si no está en features
if target in df.columns and target not in features:
    features.append(target)

# Crear el nuevo DataFrame solo con variables seleccionadas + target
df_modelo = df[features].copy()

# Guardar a Excel
#output_path = "datos_modelo_GRD.xlsx"
#df_modelo.to_excel(output_path, index=False)

#print(f"\n📁 Archivo guardado exitosamente en: {output_path}")