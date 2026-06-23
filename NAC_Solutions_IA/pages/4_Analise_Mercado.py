import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.carregar_dados import carregar_dados
from utils.treinar_modelo import clusterizar_mercados
from utils.graficos import grafico_cluster, grafico_heatmap_bairro_produto
import plotly.express as px

st.set_page_config(page_title="Análise por Mercado", page_icon="🗺️", layout="wide")
st.title("🗺️ Análise por Mercado")
st.markdown("Agrupamento e comparação de mercados por comportamento de preços.")
st.markdown("---")

df = carregar_dados()

# Clustering
st.markdown("### 🔵 Agrupamento de Mercados (K-Means)")
pivot = clusterizar_mercados(df)
st.plotly_chart(grafico_cluster(pivot), use_container_width=True)

st.markdown("### 📋 Classificação dos Mercados")
tabela_cluster = pivot[['Mercado', 'mean', 'std', 'count', 'categoria']].copy()
tabela_cluster.columns = ['Mercado', 'Preço Médio (AOA)', 'Desvio Padrão', 'Registos', 'Categoria']
tabela_cluster = tabela_cluster.round(2).sort_values('Preço Médio (AOA)', ascending=False)
st.dataframe(tabela_cluster, use_container_width=True)

st.markdown("---")
st.markdown("### 🌡️ Mapa de Calor — Preços por Bairro e Produto")
st.plotly_chart(grafico_heatmap_bairro_produto(df), use_container_width=True)

st.markdown("---")
st.markdown("### 📊 Comparação Detalhada por Mercado")
mercado_sel = st.selectbox("Selecione um Mercado:", sorted(df['Mercado'].unique()))
dados_mercado = df[df['Mercado'] == mercado_sel]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Registos", len(dados_mercado))
col2.metric("Produtos", dados_mercado['Produto'].nunique())
col3.metric("Preço Médio", f"{dados_mercado['Preco'].mean():,.0f} AOA")
col4.metric("Tipo", dados_mercado['Tipo'].mode()[0])

fig = px.bar(
    dados_mercado.groupby('Produto')['Preco'].mean().reset_index().sort_values('Preco', ascending=False).head(20),
    x='Produto', y='Preco',
    title=f'Top 20 Produtos — {mercado_sel}',
    labels={'Preco': 'Preço Médio (AOA)'},
    color='Preco', color_continuous_scale='Blues'
)
fig.update_layout(plot_bgcolor='white', xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
