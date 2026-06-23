import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.carregar_dados import carregar_dados
from utils.graficos import (grafico_preco_por_mercado, grafico_distribuicao_tipos,
                             grafico_heatmap_bairro_produto, grafico_origem)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard Geral")
st.markdown("Visão geral dos dados recolhidos nos mercados do Uíge.")
st.markdown("---")

df = carregar_dados()

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Registos", f"{len(df):,}")
col2.metric("Produtos Diferentes", df['Produto'].nunique())
col3.metric("Mercados", df['Mercado'].nunique())
col4.metric("Preço Médio (AOA)", f"{df['Preco'].mean():,.0f}")
col5.metric("Preço Máximo (AOA)", f"{df['Preco'].max():,.0f}")

st.markdown("---")

col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(grafico_preco_por_mercado(df), use_container_width=True)
with col_b:
    st.plotly_chart(grafico_distribuicao_tipos(df), use_container_width=True)

st.plotly_chart(grafico_origem(df), use_container_width=True)

st.markdown("### 🗃️ Tabela de Dados")
st.dataframe(
    df[['Codigo', 'Data', 'Mercado', 'Tipo', 'Produto', 'Preco', 'Origem', 'Bairro', 'Zona']].head(50),
    use_container_width=True
)

st.markdown("---")
st.markdown("### 📋 Estatísticas Descritivas")
st.dataframe(df.groupby('Mercado')['Preco'].describe().round(2), use_container_width=True)
