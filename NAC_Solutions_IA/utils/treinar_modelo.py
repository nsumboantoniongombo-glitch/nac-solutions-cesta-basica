import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.cluster import KMeans

# Caminho para guardar modelo (funciona local, ignorado no cloud)
CAMINHO_MODELO = os.path.join(os.path.dirname(__file__), '..', 'models', 'modelo_preco.pkl')

# Cache em memória para o Streamlit Cloud
_MODELO_CACHE = None

def preparar_features(df):
    df_model = df[['Mercado', 'Tipo', 'Produto', 'Origem', 'Bairro', 'Zona', 'Preco']].dropna().copy()
    encoders = {}
    for col in ['Mercado', 'Tipo', 'Produto', 'Origem', 'Bairro', 'Zona']:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col].astype(str))
        encoders[col] = le
    return df_model, encoders

def treinar_modelo_regressao(df):
    global _MODELO_CACHE
    df_model, encoders = preparar_features(df)
    X = df_model[['Mercado', 'Tipo', 'Produto', 'Origem', 'Bairro', 'Zona']]
    y = df_model['Preco']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    dados_modelo = {'modelo': modelo, 'encoders': encoders, 'mae': mae, 'r2': r2}
    # Guardar em memória
    _MODELO_CACHE = dados_modelo
    # Tentar guardar em disco (funciona local, falha silenciosa no cloud)
    try:
        with open(CAMINHO_MODELO, 'wb') as f:
            pickle.dump(dados_modelo, f)
    except Exception:
        pass
    return mae, r2

def carregar_modelo():
    global _MODELO_CACHE
    # Primeiro verifica memória
    if _MODELO_CACHE is not None:
        return _MODELO_CACHE
    # Depois tenta disco
    if os.path.exists(CAMINHO_MODELO):
        if os.path.getsize(CAMINHO_MODELO) == 0:
            return None
        try:
            with open(CAMINHO_MODELO, 'rb') as f:
                _MODELO_CACHE = pickle.load(f)
                return _MODELO_CACHE
        except Exception:
            return None
    return None

def prever_preco(mercado, tipo, produto, origem, bairro, zona):
    dados = carregar_modelo()
    if dados is None:
        return None
    modelo = dados['modelo']
    encoders = dados['encoders']
    try:
        entrada = pd.DataFrame([[mercado, tipo, produto, origem, bairro, zona]],
                               columns=['Mercado', 'Tipo', 'Produto', 'Origem', 'Bairro', 'Zona'])
        for col in entrada.columns:
            le = encoders[col]
            val = entrada[col][0]
            if val in le.classes_:
                entrada[col] = le.transform([val])
            else:
                entrada[col] = le.transform([le.classes_[0]])
        preco = modelo.predict(entrada)[0]
        return round(preco, 2)
    except Exception:
        return None

def detectar_anomalias(df):
    df_model = df[['Preco']].dropna().copy()
    iso = IsolationForest(contamination=0.05, random_state=42)
    df_model['anomalia'] = iso.fit_predict(df_model[['Preco']])
    indices = df_model[df_model['anomalia'] == -1].index
    return df.loc[indices]

def clusterizar_mercados(df):
    pivot = df.groupby('Mercado')['Preco'].agg(['mean', 'std', 'count']).dropna()
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    pivot['cluster'] = kmeans.fit_predict(pivot[['mean', 'std']])
    centros = kmeans.cluster_centers_
    ordem = centros[:, 0].argsort()
    mapa = {ordem[0]: 'Preços Baixos', ordem[1]: 'Preços Médios', ordem[2]: 'Preços Altos'}
    pivot['categoria'] = pivot['cluster'].map(mapa)
    return pivot.reset_index()
