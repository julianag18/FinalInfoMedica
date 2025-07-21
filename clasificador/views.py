from django.shortcuts import render
from .forms import PrediccionGRDForm
import joblib
import json
import pandas as pd
import numpy as np

# Cargar modelo y transformadores
modelo = joblib.load('clasificador/modelo_grd.pkl')
scaler = joblib.load('clasificador/scaler.pkl')
labelencoder = joblib.load('clasificador/labelencoder.pkl')
with open('clasificador/columnas_modelo.json', 'r') as f:
    columnas_modelo = json.load(f)

def predecir_grd(request):
    resultado = None
    if request.method == 'POST':
        form = PrediccionGRDForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            df = pd.DataFrame([datos])
            df.fillna('Desconocido', inplace=True)
            df_dummies = pd.get_dummies(df)

            # Asegurar columnas del modelo
            for col in columnas_modelo:
                if col not in df_dummies.columns:
                    df_dummies[col] = 0
            df_dummies = df_dummies[columnas_modelo]

            # Escalar
            X_scaled = scaler.transform(df_dummies)

            # Predecir
            pred = modelo.predict(X_scaled)
            resultado = labelencoder.inverse_transform(pred)[0]

    else:
        form = PrediccionGRDForm()

    return render(request, 'formulario.html', {'form': form, 'resultado': resultado})


