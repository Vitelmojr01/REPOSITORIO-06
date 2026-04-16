import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set(context='talk', style='ticks')

st.set_page_config(
    page_title="Previsão de Renda",
    page_icon="💰",
    layout="wide",
)

st.title("Análise Exploratória da Previsão de Renda")
st.write("Aplicação em Streamlit baseada no notebook completo do Projeto 2.")

@st.cache_data
def carregar_dados():
    df = pd.read_csv('previsao_de_renda.csv')
    df['data_ref'] = pd.to_datetime(df['data_ref'])
    return df

renda = carregar_dados()

st.subheader("Visualização inicial dos dados")
st.dataframe(renda.head())

st.subheader("Informações gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Quantidade de linhas", renda.shape[0])
col2.metric("Quantidade de colunas", renda.shape[1])
col3.metric("Renda média", f"R$ {renda['renda'].mean():.2f}")

st.subheader("Filtro de período")

data_min = renda['data_ref'].min().date()
data_max = renda['data_ref'].max().date()

periodo = st.slider(
    "Selecione o intervalo de datas",
    min_value=data_min,
    max_value=data_max,
    value=(data_min, data_max)
)

renda_filtrada = renda[
    (renda['data_ref'].dt.date >= periodo[0]) &
    (renda['data_ref'].dt.date <= periodo[1])
].copy()

st.subheader("Distribuição da renda")

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(renda_filtrada['renda'], kde=True, ax=ax)
ax.set_title("Distribuição da renda")
ax.set_xlabel("Renda")
ax.set_ylabel("Frequência")
sns.despine()
st.pyplot(fig)

st.subheader("Análise ao longo do tempo")

variavel_tempo = st.selectbox(
    "Escolha a variável para analisar ao longo do tempo",
    [
        'posse_de_imovel',
        'posse_de_veiculo',
        'qtd_filhos',
        'tipo_renda',
        'educacao',
        'estado_civil',
        'tipo_residencia'
    ]
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='data_ref',
    y='renda',
    hue=variavel_tempo,
    data=renda_filtrada,
    ax=ax
)
ax.set_title(f"Renda ao longo do tempo por {variavel_tempo}")
ax.set_xlabel("Data")
ax.set_ylabel("Renda")
ax.tick_params(axis='x', rotation=45)
sns.despine()
st.pyplot(fig)

st.subheader("Análise bivariada")

variavel_bivariada = st.selectbox(
    "Escolha a variável para comparar com a renda",
    [
        'posse_de_imovel',
        'posse_de_veiculo',
        'qtd_filhos',
        'tipo_renda',
        'educacao',
        'estado_civil',
        'tipo_residencia'
    ],
    index=1
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=variavel_bivariada,
    y='renda',
    data=renda_filtrada,
    ax=ax
)
ax.set_title(f"Renda média por {variavel_bivariada}")
ax.set_xlabel(variavel_bivariada)
ax.set_ylabel("Renda média")
ax.tick_params(axis='x', rotation=45)
sns.despine()
st.pyplot(fig)

st.subheader("Resumo estatístico")
st.dataframe(renda_filtrada[['renda', 'idade', 'tempo_emprego', 'qt_pessoas_residencia']].describe())

st.subheader("Insight automático")

media_por_categoria = (
    renda_filtrada.groupby(variavel_bivariada)['renda']
    .mean()
    .sort_values(ascending=False)
)

if len(media_por_categoria) > 0:
    melhor_categoria = media_por_categoria.index[0]
    maior_media = media_por_categoria.iloc[0]

    st.write(
        f"A categoria com maior renda média em **{variavel_bivariada}** é "
        f"**{melhor_categoria}**, com renda média de **R$ {maior_media:.2f}**."
    )

st.subheader("Tabela filtrada")
st.dataframe(renda_filtrada)