import pandas as pd
import os

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), '..', 'data', 'dados_uige.xlsx')

def carregar_dados():
    df = pd.read_excel(CAMINHO_DADOS, sheet_name='Dados Uíge', skiprows=2)
    df.columns = ['Codigo', 'Data', 'Hora', 'Mercado', 'Tipo', 'Produto', 'Preco', 'Origem', 'Bairro', 'Zona']
    df = df.dropna(subset=['Codigo'])
    df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    return df

def obter_produtos(df):
    return sorted(df['Produto'].dropna().unique().tolist())

def obter_mercados(df):
    return sorted(df['Mercado'].dropna().unique().tolist())

def obter_bairros(df):
    return sorted(df['Bairro'].dropna().unique().tolist())

def obter_tipos(df):
    return sorted(df['Tipo'].dropna().unique().tolist())

def obter_origens(df):
    return sorted(df['Origem'].dropna().unique().tolist())
