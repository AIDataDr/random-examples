from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image

ROOT = Path(__file__).resolve().parent
logo = Image.open(ROOT / 'assets/logo.png')
st.set_page_config(page_title='My Analytics Application', page_icon=logo, layout='wide', initial_sidebar_state='expanded')
st.sidebar.image(logo, width=75)
st.sidebar.header('Settings')
mean = st.sidebar.slider('Mean', 0, 100, 50)
std = st.sidebar.slider('Standard deviation', 1, 30, 10)
n = st.sidebar.slider('Sample size', 100, 10000, 1000)
st.title('My Analytics Dashboard')
st.write('A Streamlit desktop application using pywebview.')
data = np.random.default_rng(42).normal(mean, std, n)
df = pd.DataFrame({'Value': data})
a, b, c = st.columns(3)
a.metric('Sample size', n)
b.metric('Mean', f'{data.mean():.2f}')
c.metric('Standard deviation', f'{data.std():.2f}')
st.plotly_chart(px.histogram(df, x='Value', nbins=40, title='Sample Distribution'))
with st.expander('View underlying data'):
    st.dataframe(df)
