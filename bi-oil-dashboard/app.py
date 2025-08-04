import streamlit as st
import pandas as pd
import plotly.express as px

st.title("BI-дашборд для анализа скважин")

# Загрузка данных
uploaded_file = st.file_uploader("Загрузите CSV файл с данными", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])  # Предполагаем, что есть колонка 'date'
    
    # Фильтр по дате
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = st.slider("Выберите период", min_value=min_date, max_value=max_date,
                           value=(min_date, max_date))
    df_filtered = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
    
    # Фильтр по скважинам
    wells = df_filtered['well_id'].unique()
    selected_wells = st.multiselect("Выберите скважины", wells, default=wells.tolist())
    df_filtered = df_filtered[df_filtered['well_id'].isin(selected_wells)]
    
    # Линейный график давления
    st.subheader("Давление по времени")
    fig_pressure = px.line(df_filtered, x='date', y='pressure', color='well_id',
                           labels={'pressure': 'Давление, бар', 'date': 'Дата'})
    st.plotly_chart(fig_pressure, use_container_width=True)
    
    # Линейный график обводнения
    st.subheader("Обводнение по времени")
    fig_watercut = px.line(df_filtered, x='date', y='watercut', color='well_id',
                           labels={'watercut': 'Обводнение, %', 'date': 'Дата'})
    st.plotly_chart(fig_watercut, use_container_width=True)
    
    # Scatter plot для сравнения давления и обводнения
    st.subheader("Зависимость давления и обводнения")
    fig_scatter = px.scatter(df_filtered, x='pressure', y='watercut', color='well_id',
                             labels={'pressure': 'Давление, бар', 'watercut': 'Обводнение, %'})
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Пожалуйста, загрузите CSV файл с данными.")
