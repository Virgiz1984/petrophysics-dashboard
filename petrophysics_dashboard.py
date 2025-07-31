# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 11:18:04 2025

@author: rudenko
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Игрушечный дашборд по петрофизике")

# Генерируем пример данных
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'Скважина': [f'Well_{i+1}' for i in range(n)],
    'Пористость, %': np.random.normal(15, 5, n).clip(0, 40),
    'Проницаемость, мкм²': np.random.normal(100, 50, n).clip(1, 300),
    'Насыщенность, %': np.random.uniform(0, 1000, n),
})

# Фильтр по пористости
min_phi, max_phi = st.slider('Диапазон пористости (%)', 0, 40, (5, 25))

filtered_data = data[(data['Пористость, %'] >= min_phi) & (data['Пористость, %'] <= max_phi)]

st.write(f"Отфильтровано скважин: {filtered_data.shape[0]}")
st.dataframe(filtered_data)

# Гистограмма пористости
st.subheader('Гистограмма пористости')
fig, ax = plt.subplots()
sns.histplot(filtered_data['Пористость, %'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# График проницаемость vs пористость
st.subheader('Проницаемость vs Пористость')
fig2, ax2 = plt.subplots()
sns.scatterplot(x='Пористость, %', y='Проницаемость, мкм²', data=filtered_data, ax=ax2)
st.pyplot(fig2)

# Выбор конкретной скважины
well_selected = st.selectbox('Выберите скважину для подробностей', filtered_data['Скважина'].tolist())

if well_selected:
    well_data = filtered_data[filtered_data['Скважина'] == well_selected].iloc[0]
    st.write(f"Данные по скважине **{well_selected}**:")
    st.write(f" - Пористость: {well_data['Пористость, %']:.2f} %")
    st.write(f" - Проницаемость: {well_data['Проницаемость, мкм²']:.2f} мкм²")
    st.write(f" - Насыщенность: {well_data['Насыщенность, %']:.2f} %")
