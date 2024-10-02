import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from datetime import datetime
import pandas as pd


def convert_format_datetime(data):
    data['start_time'] = pd.to_datetime(data['start_time'])
    data['end_time'] = pd.to_datetime(data['end_time'])
    data['duration'] = (data['end_time'] - data['start_time']).dt.total_seconds() / 60  # Duración en minutos
    data['date'] = data['start_time'].dt.date
    return data[['concentration_type', 'subconcentration_type', 'duration', 'date']]

def generate_grouped_data(data):
    data = convert_format_datetime(data)
    
    total_per_day = data.groupby(['date'])['duration'].sum().reset_index()
    total_per_day_per_type = data.groupby(['date', 'concentration_type'])['duration'].sum().reset_index()
    
    sub_grouped_data = {}
    for concentration in data['concentration_type'].unique():
        sub_grouped_data[concentration] = data[data['concentration_type'] == concentration] \
                                             .groupby(['date', 'subconcentration_type'])['duration'].sum().reset_index()
    
    return total_per_day, total_per_day_per_type, sub_grouped_data


def generate_combined_line_plots(total_per_day, total_per_day_per_type):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Tiempo Total por Día", "Tiempo de Concentración por Tipo"))

    # Gráfico de tiempo total por día
    fig.add_trace(
        go.Scatter(x=total_per_day['date'], y=total_per_day['duration'], mode='lines+markers', name='Total por Día'),
        row=1, col=1
    )

    # Gráfico de tiempo de concentración por tipo
    for concentration_type, df_subset in total_per_day_per_type.groupby('concentration_type'):
        fig.add_trace(
            go.Scatter(x=df_subset['date'], y=df_subset['duration'], mode='lines+markers', name=concentration_type),
            row=1, col=2
        )

    fig.update_layout(
        height=600,
        width=1200,
        title_text="Gráficos de Tiempo de Concentración",
        xaxis_title="Fecha",
        yaxis_title="Tiempo Total (minutos)",
        template='plotly_white'
    )

    # Formato de fecha y rotación
    for col in [1, 2]:
        fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=-45, row=1, col=col)

    fig.show()


def generate_subgroup_plots(sub_grouped_data):
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Estudio", "Meditación", "Ejercicio Físico", "Trabajo"))

    concentration_types = ['Estudio', 'Meditación', 'Ejercicio Físico', 'Trabajo']
    rows = [1, 1, 2, 2]
    cols = [1, 2, 1, 2]

    for i, concentration in enumerate(concentration_types):
        df_subset = sub_grouped_data[concentration]
        for subconcentration in df_subset['subconcentration_type'].unique():
            df_filtered = df_subset[df_subset['subconcentration_type'] == subconcentration]
            fig.add_trace(
                go.Scatter(x=df_filtered['date'], y=df_filtered['duration'], mode='lines+markers', name=f'{concentration} - {subconcentration}'),
                row=rows[i], col=cols[i]
            )

    fig.update_layout(height=800, width=1000, title_text="Gráficos de tiempo por tipo de concentración")
    fig.update_xaxes(tickformat="%d-%m-%Y", tickangle=45)  # Formato día-mes-año
    fig.show()


# Usar las funciones para obtener los datos y generar el gráfico

# from database import TemporizadorDB 

# db = TemporizadorDB()
# data = db.get_sessions_with_label()
# db.close()

# total_per_day, total_per_day_per_type, sub_grouped_data = generate_grouped_data(data)

# generate_combined_line_plots(total_per_day, total_per_day_per_type)
# generate_subgroup_plots(sub_grouped_data)
