# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:10:41 2024

@author: crist
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# URL del JSON
#Risky
#url = 'https://fintual.cl/api/real_assets/186/days'
#Streep
url = 'https://fintual.cl/api/real_assets/15077/days'

# Obtener los datos
response = requests.get(url)
data = response.json()

# Extraer fechas y precios
dates = [item['attributes']['date'] for item in data['data']]
prices = [item['attributes']['price'] for item in data['data']]

# Crear un DataFrame de pandas
df = pd.DataFrame({'Date': dates, 'Price': prices})

# Convertir la columna 'Date' a datetime
df['Date'] = pd.to_datetime(df['Date'])

# Ordenar el DataFrame por fecha
df.sort_values('Date', inplace=True)

# Calcular la media móvil de 200 periodos
df['200_MA'] = df['Price'].rolling(window=200).mean()

# Función para calcular el RSI
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calcular el RSI para el precio
df['RSI'] = calculate_rsi(df['Price'])

# Filtrar los últimos 120 días para la visualización
df_last_120_days = df[-365:]

# Función para calcular el cambio porcentual
def calculate_percentage_change(initial_price, final_price):
    return ((final_price - initial_price) / initial_price) * 100

# Calcular el cambio porcentual desde el primer hasta el último día ploteado
percentage_change = calculate_percentage_change(df_last_120_days['Price'].iloc[0], df_last_120_days['Price'].iloc[-1])

# Crear subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), dpi=100, gridspec_kw={'height_ratios': [3, 1]})

# Graficar el precio y la media móvil en el primer subplot usando los últimos 120 días
ax1.plot(df_last_120_days['Date'], df_last_120_days['Price'], color='black', label=f'Precio (Cambio: {percentage_change:.2f}%)')
ax1.plot(df_last_120_days['Date'], df_last_120_days['200_MA'], color='red', label='200 SMA')
ax1.legend()
ax1.set_title('Fintual - Risky Norris')

# Graficar el RSI en el segundo subplot usando los últimos 120 días
ax2.plot(df_last_120_days['Date'], df_last_120_days['RSI'], color='purple', label='RSI')
ax2.axhline(70, linestyle='--', color='grey', linewidth=0.5)
ax2.axhline(30, linestyle='--', color='grey', linewidth=0.5)
ax2.set_ylim(0, 100)
ax2.legend()
ax2.set_title('RSI (14) (Last 120 Days)')

plt.tight_layout()
plt.show()
