import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COR_PRIMARIA = "#1B4F72"
COR_SECUNDARIA = "#2E86C1"
COR_ALERTA = "#E74C3C"
COR_SUCESSO = "#27AE60"

def grafico_preco_por_mercado(df):
    dados = df.groupby('Mercado')['Preco'].mean().reset_index()
    dados.columns = ['Mercado', 'Preço Médio (AOA)']
    dados = dados.sort_values('Preço Médio (AOA)', ascending=False)
    fig = px.bar(dados, x='Mercado', y='Preço Médio (AOA)',
                 title='Preço Médio por Mercado',
                 color='Preço Médio (AOA)',
                 color_continuous_scale='Blues',
                 text_auto='.0f')
    fig.update_layout(showlegend=False, plot_bgcolor='white')
    return fig

def grafico_distribuicao_tipos(df):
    dados = df['Tipo'].value_counts().reset_index()
    dados.columns = ['Tipo', 'Quantidade']
    fig = px.pie(dados, names='Tipo', values='Quantidade',
                 title='Distribuição por Tipo de Mercado',
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    return fig

def grafico_produto_por_mercado(df, produto):
    dados = df[df['Produto'] == produto].copy()
    fig = px.bar(dados, x='Mercado', y='Preco',
                 title=f'Preço de "{produto}" por Mercado',
                 color='Tipo',
                 barmode='group',
                 labels={'Preco': 'Preço (AOA)'},
                 text_auto='.0f')
    fig.update_layout(plot_bgcolor='white')
    return fig

def grafico_boxplot_produto(df, produto):
    dados = df[df['Produto'] == produto]
    fig = px.box(dados, x='Mercado', y='Preco',
                 title=f'Dispersão de Preços — {produto}',
                 color='Mercado',
                 labels={'Preco': 'Preço (AOA)'})
    fig.update_layout(plot_bgcolor='white', showlegend=False)
    return fig

def grafico_evolucao_temporal(df, produto):
    dados = df[df['Produto'] == produto].dropna(subset=['Data'])
    dados = dados.sort_values('Data')
    fig = px.line(dados, x='Data', y='Preco', color='Mercado',
                  title=f'Evolução do Preço — {produto}',
                  labels={'Preco': 'Preco (AOA)', 'Data': 'Data'})
    fig.update_layout(plot_bgcolor='white')
    return fig

def grafico_heatmap_bairro_produto(df):
    pivot = df.pivot_table(values='Preco', index='Bairro', columns='Produto', aggfunc='mean')
    pivot = pivot.fillna(0)
    fig = px.imshow(pivot,
                    title='Mapa de Calor — Preço Médio por Bairro e Produto',
                    color_continuous_scale='Blues',
                    aspect='auto')
    fig.update_layout(height=500)
    return fig

def grafico_origem(df):
    dados = df.groupby(['Origem', 'Mercado'])['Preco'].mean().reset_index()
    fig = px.bar(dados, x='Mercado', y='Preco', color='Origem',
                 barmode='group',
                 title='Preço Médio por Origem e Mercado',
                 labels={'Preco': 'Preço Médio (AOA)'},
                 color_discrete_map={'Nacional': COR_SUCESSO, 'Importado': COR_ALERTA})
    fig.update_layout(plot_bgcolor='white')
    return fig

def grafico_anomalias(df, anomalias):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Preco'],
        mode='markers', name='Normal',
        marker=dict(color=COR_SECUNDARIA, size=4, opacity=0.5)
    ))
    fig.add_trace(go.Scatter(
        x=anomalias.index, y=anomalias['Preco'],
        mode='markers', name='Anomalia',
        marker=dict(color=COR_ALERTA, size=10, symbol='x')
    ))
    fig.update_layout(title='Detecção de Anomalias nos Preços',
                      xaxis_title='Registo', yaxis_title='Preço (AOA)',
                      plot_bgcolor='white')
    return fig

def grafico_cluster(pivot):
    cores = {'Preços Baixos': '#27AE60', 'Preços Médios': '#F39C12', 'Preços Altos': '#E74C3C'}
    fig = px.scatter(pivot, x='mean', y='std',
                     color='categoria', text='Mercado',
                     title='Agrupamento de Mercados por Comportamento de Preço',
                     labels={'mean': 'Preço Médio (AOA)', 'std': 'Variação de Preço'},
                     color_discrete_map=cores, size='count')
    fig.update_traces(textposition='top center')
    fig.update_layout(plot_bgcolor='white')
    return fig
