import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Cargar el dataset
df = pd.read_csv('nba_all_elo.csv')

# Barra lateral con título
st.sidebar.title("Seleccionar un año y equipo:")

# Barra lateral para seleccionar el año
year = st.sidebar.selectbox('Año', df['year_id'].unique())

# Barra lateral para seleccionar un equipo
team = st.sidebar.selectbox('Equipo', df['team_id'].unique())

# Barra lateral para seleccionar el tipo de juego con "pills" (botones)
game_type = st.sidebar.radio(
    'Temporada Regular, Playoffs o Ambos:',
    ['Regular', 'Playoffs', 'Ambos'],
    index=0  # Establecer la opción predeterminada
)

# Filtrar los datos según las selecciones
filtered_data = df[(df['year_id'] == year) & (df['team_id'] == team)]
if game_type != 'Ambos':
    filtered_data = filtered_data[filtered_data['is_playoffs'] == (1 if game_type == 'Playoffs' else 0)]

# Contar juegos ganados y perdidos
wins = filtered_data[filtered_data['game_result'] == 'W'].groupby('date_game').size().cumsum()
losses = filtered_data[filtered_data['game_result'] == 'L'].groupby('date_game').size().cumsum()

# Crear una figura con dos subgráficas
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))

# Gráfica de líneas (Juegos Ganados vs Perdidos)
ax1.plot(wins.index, wins.values, label="Juegos Ganados", color='g')
ax1.plot(losses.index, losses.values, label="Juegos Perdidos", color='r')
ax1.set_title(f'Juegos Ganados vs Perdidos en {year} para {team}')
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Acumulado')
ax1.legend()

# Calcular los porcentajes de juegos ganados y perdidos
total_games = len(filtered_data)
wins_count = len(filtered_data[filtered_data['game_result'] == 'W'])
losses_count = total_games - wins_count

# Gráfica de pastel (Porcentaje de Juegos Ganados y Perdidos)
labels = ['Juegos Ganados', 'Juegos Perdidos']
sizes = [wins_count, losses_count]
colors = ['gold', 'lightcoral']
ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax2.set_title(f'Porcentaje de Juegos Ganados y Perdidos en {year} para {team}')

# Mostrar las gráficas en Streamlit
st.pyplot(fig)
