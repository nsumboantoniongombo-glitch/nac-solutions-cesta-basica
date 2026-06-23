import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.carregar_dados import carregar_dados
from utils.treinar_modelo import detectar_anomalias
from utils.graficos import grafico_anomalias
import plotly.express as px

st.set_page_config(page_title="Detecção de Anomalias", page_icon="⚠️", layout="wide")
st.title("⚠️ Detecção de Anomalias de Preços")
st.markdown("Identificação automática de preços suspeitos ou fora do padrão usando Isolation Forest.")
st.markdown("---")

df = carregar_dados()

anomalias = detectar_anomalias(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total de Registos", len(df))
col2.metric("Anomalias Detectadas", len(anomalias), delta=f"{len(anomalias)/len(df)*100:.1f}%")
col3.metric("Registos Normais", len(df) - len(anomalias))

st.markdown("---")
st.plotly_chart(grafico_anomalias(df, anomalias), use_container_width=True)

st.markdown("### ⚠️ Registos com Preços Anómalos")
if not anomalias.empty:
    st.dataframe(
        anomalias[['Codigo', 'Data', 'Mercado', 'Tipo', 'Produto', 'Preco', 'Origem', 'Bairro']].sort_values('Preco', ascending=False),
        use_container_width=True
    )

    st.markdown("### 📊 Anomalias por Mercado")
    fig = px.bar(
        anomalias['Mercado'].value_counts().reset_index(),
        x='Mercado', y='count',
        title='Número de Anomalias por Mercado',
        labels={'count': 'Nº de Anomalias'},
        color='count', color_continuous_scale='Reds'
    )
    fig.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📦 Produtos com Mais Anomalias")
    fig2 = px.bar(
        anomalias['Produto'].value_counts().head(10).reset_index(),
        x='Produto', y='count',
        title='Top 10 Produtos com Preços Anómalos',
        labels={'count': 'Nº de Anomalias'},
        color='count', color_continuous_scale='Oranges'
    )
    fig2.update_layout(plot_bgcolor='white', xaxis_tickangle=-30)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.success("Nenhuma anomalia detectada nos dados actuais.")
