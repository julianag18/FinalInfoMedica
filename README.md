# FinalInfoMedica
Informática Médica
El archivo informeEDA.ipynb contiene todo el análisis estadístico de las variables dadas y como se llegó a la base de datos posteriormente usada en la parte de Django.

Los archivos llamados juli.ipynb, julianapruebas.ipynb, pruebas_redes.ipynb, pruebas.ipynb son todos de prueba y error de diferentes modelos de redes neuronales con variación de hiperparámetros y parámetros, se pueden ignorar. Se adjuntaron solo para demostrar el arduo trabajo y la dedicación que se le puso a este proyecto.

El archivo finalinformaticamedica.ipynb es donde se creó el modelo final de redes neuronales obteniendo un 80% de precisión, aquí se filtró de manera automática la base de datos virgen, conservando solo las columnas o claves con al menos el 2% de de datos no nulos para así tener una reducción en claves que no estaban aportando nada y estaban aprendiendo a la vez que reduciendo la precisión del modelo. Sin embargo, este archivo no se usó para el modelo de django
