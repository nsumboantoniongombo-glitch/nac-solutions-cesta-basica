import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.carregar_dados import carregar_dados, obter_produtos, obter_mercados, obter_bairros, obter_tipos, obter_origens
from utils.treinar_modelo import treinar_modelo_regressao, prever_preco, carregar_modelo

st.set_page_config(page_title="Previsão com IA", page_icon="🤖", layout="wide")
st.title("🤖 Previsão de Preços com Inteligência Artificial")
st.markdown("Utilize o modelo treinado com Random Forest para prever o preço de um produto.")
st.markdown("---")

df = carregar_dados()

# Treinar modelo se não existir
modelo_dados = carregar_modelo()
if modelo_dados is None:
    with st.spinner("A treinar o modelo de IA pela primeira vez..."):
        mae, r2 = treinar_modelo_regressao(df)
    st.success(f"Modelo treinado com sucesso! MAE: {mae:.0f} AOA | R²: {r2:.2f}")
    modelo_dados = carregar_modelo()

# Métricas do modelo
if modelo_dados:
    col1, col2, col3 = st.columns(3)
    col1.metric("Algoritmo", "Random Forest")
    col2.metric("Erro Médio (MAE)", f"{modelo_dados['mae']:.0f} AOA")
    col3.metric("Precisão (R²)", f"{modelo_dados['r2']:.2%}")

st.markdown("---")
st.markdown("### 🔮 Fazer Previsão")

col_a, col_b = st.columns(2)

with col_a:
    produto_sel = st.selectbox("Produto:", obter_produtos(df))
    mercado_sel = st.selectbox("Mercado:", obter_mercados(df))
    tipo_sel = st.selectbox("Tipo de Mercado:", obter_tipos(df))

with col_b:
    origem_sel = st.selectbox("Origem:", obter_origens(df))
    bairro_sel = st.selectbox("Bairro:", obter_bairros(df))
    zona_sel = st.selectbox("Zona:", sorted(df['Zona'].dropna().unique().tolist()))

st.markdown("---")

if st.button("🤖 Prever Preço", type="primary", use_container_width=True):
    preco_previsto = prever_preco(mercado_sel, tipo_sel, produto_sel, origem_sel, bairro_sel, zona_sel)
    if preco_previsto:
        st.success(f"### 💰 Preço Previsto: **{preco_previsto:,.0f} AOA**")

        # Comparar com preço real
        dados_reais = df[(df['Produto'] == produto_sel) & (df['Mercado'] == mercado_sel)]
        if not dados_reais.empty:
            preco_real_medio = dados_reais['Preco'].mean()
            diferenca = preco_previsto - preco_real_medio
            st.info(f"📊 Preço real médio neste mercado: **{preco_real_medio:,.0f} AOA** | Diferença: **{diferenca:+,.0f} AOA**")
    else:
        st.error("Não foi possível fazer a previsão. Verifique se o modelo está treinado.")

st.markdown("---")
st.markdown("### 🔄 Re-treinar Modelo")
if st.button("Re-treinar Modelo com Dados Actuais", use_container_width=True):
    with st.spinner("A re-treinar o modelo..."):
        mae, r2 = treinar_modelo_regressao(df)
    st.success(f"Modelo re-treinado! MAE: {mae:.0f} AOA | R²: {r2:.2f}")
