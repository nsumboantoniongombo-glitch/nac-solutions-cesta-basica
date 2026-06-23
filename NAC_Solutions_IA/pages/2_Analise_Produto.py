import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.carregar_dados import carregar_dados, obter_produtos
from utils.graficos import (grafico_produto_por_mercado, grafico_boxplot_produto,
                             grafico_evolucao_temporal)

st.set_page_config(page_title="Análise por Produto", page_icon="🔍", layout="wide")
st.title("🔍 Análise por Produto")
st.markdown("Selecione um produto para comparar os seus preços em todos os mercados.")
st.markdown("---")

df = carregar_dados()
produtos = obter_produtos(df)

produto_sel = st.selectbox("Selecione o Produto:", produtos)

if produto_sel:
    dados_produto = df[df['Produto'] == produto_sel]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Preço Mínimo", f"{dados_produto['Preco'].min():,.0f} AOA")
    col2.metric("Preço Máximo", f"{dados_produto['Preco'].max():,.0f} AOA")
    col3.metric("Preço Médio", f"{dados_produto['Preco'].mean():,.0f} AOA")
    col4.metric("Registos", len(dados_produto))

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(grafico_produto_por_mercado(df, produto_sel), use_container_width=True)
    with col_b:
        st.plotly_chart(grafico_boxplot_produto(df, produto_sel), use_container_width=True)

    st.plotly_chart(grafico_evolucao_temporal(df, produto_sel), use_container_width=True)

    st.markdown("### 📋 Dados do Produto por Mercado")
    tabela = dados_produto.groupby('Mercado')['Preco'].agg(['min', 'max', 'mean', 'count'])
    tabela.columns = ['Mínimo (AOA)', 'Máximo (AOA)', 'Média (AOA)', 'Registos']
    tabela = tabela.round(2)
    st.dataframe(tabela, use_container_width=True)

    st.markdown("### 📄 Registos Detalhados")
    st.dataframe(
        dados_produto[['Codigo', 'Data', 'Mercado', 'Tipo', 'Preco', 'Origem', 'Bairro']].sort_values('Preco'),
        use_container_width=True
    )
