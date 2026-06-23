import streamlit as st

st.set_page_config(
    page_title="NAC Solutions — Cesta Básica Uíge",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image("assets/logo.png", use_column_width=True) if __import__('os').path.exists("assets/logo.png") else None

st.sidebar.markdown("""
# 📊 NAC Solutions
### Portal de Análise de Preços
**Província do Uíge — 2026**
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Navegação:**
- 📊 Dashboard Geral
- 🔍 Análise por Produto
- 🤖 Previsão com IA
- 🗺️ Análise por Mercado
- ⚠️ Detecção de Anomalias
""")

st.sidebar.markdown("---")
st.sidebar.caption("Universidade Kimpa Vita\nEscola Superior Politécnico do Uíge\nCurso de Engenharia Informática — 3º Ano")

st.title("📊 NAC Solutions — Disparidade de Preços da Cesta Básica")
st.markdown("""
### Bem-vindo ao Portal de Análise de Preços do Uíge

Este sistema utiliza **Inteligência Artificial** para analisar a disparidade de preços
dos produtos da cesta básica em diferentes mercados da Província do Uíge.

---

#### 🗂️ Selecione uma página no menu lateral para começar:

| Página | Descrição |
|--------|-----------|
| 📊 **Dashboard** | Visão geral estatística dos dados recolhidos |
| 🔍 **Análise por Produto** | Compare preços de um produto em todos os mercados |
| 🤖 **Previsão com IA** | Preveja o preço de um produto usando Machine Learning |
| 🗺️ **Análise por Mercado** | Agrupamento e comparação entre mercados |
| ⚠️ **Anomalias** | Detecção automática de preços suspeitos |

---
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("📍 **Local:** Uíge, Angola")
with col2:
    st.info("📅 **Período:** Abril — Junho 2026")
with col3:
    st.info("👥 **Grupo:** NAC Solutions")
