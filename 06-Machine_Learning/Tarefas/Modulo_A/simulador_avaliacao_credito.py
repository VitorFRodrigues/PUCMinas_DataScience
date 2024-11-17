import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador

##########################################################################
# Download de Objetos: Modelos costumam ser muito grandes para permanecer no github.
import requests
from joblib import load
from io import BytesIO

# Link compartilhado do OneDrive
onedrive_url = "https://1drv.ms/u/s!Ag9v3Du8Ydbojtk2qojwhL6y48jrDQ?e=LbWyWI"

# Função para ajustar o link do OneDrive para download direto
def ajustar_link_onedrive(url):
    # Transformar o link de compartilhamento em link de download
    if "1drv.ms" in url:
        response = requests.get(url, allow_redirects=False)
        if "Location" in response.headers:
            return response.headers["Location"]
    return url

# Função para baixar o modelo e carregá-lo diretamente na memória
def carregar_modelo_from_onedrive(url):
    # Ajustar o link para download direto
    download_url = ajustar_link_onedrive(url)
    
    # Fazer o download do arquivo
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        # Carregar o conteúdo do arquivo diretamente na memória
        file_like_object = BytesIO(response.content)
        model = load(file_like_object)  # Carregar o modelo diretamente da memória
        print("Modelo carregado com sucesso da memória")
        return model
    else:
        print(f"Erro ao baixar o modelo: {response.status_code}")
        return None

########################################################################## 

# Definir estilo para o listbox
st.markdown(
    '<style>div[data-baseweb="select"] > div {background-color: #eee1f79e;}</style>',
    unsafe_allow_html=True
)

# Função para avaliação
def avaliar_mau(dict_respostas):
    # print(carregar_modelo_from_onedrive(onedrive_url))
    # modelo = carregar_modelo_from_onedrive(onedrive_url)
    modelo = load('Objeto/modelo_RandomForest.joblib')
    features = load('Objeto/features.joblib')

    if dict_respostas['ANOS_DESEMPREGADO'] > 0:
        dict_respostas['ANOS_EMPREGADO'] = dict_respostas['ANOS_DESEMPREGADO'] * -1 

    respostas = [dict_respostas.get(col, 0) for col in features]

    df_novo_cliente = pd.DataFrame([respostas], columns=features)

    mau = modelo.predict(df_novo_cliente)[0]

    return mau

# Exibição do logotipo e título
st.image('img/bytebank_logo.png')
st.title("Simulador de Avaliação de Crédito")

# Expansores para categorias
my_expander_1 = st.expander("Trabalho")
my_expander_2 = st.expander("Pessoal")
my_expander_3 = st.expander("Família")

# Dicionário para respostas
dict_respostas = {}
lista_campos = load(r'Objeto/lista_campos.joblib')

# Expansor 1: Trabalho
with my_expander_1:
    col1_form, col2_form = st.columns(2)

    dict_respostas['CATEGORIA_RENDA'] = col1_form.selectbox(
        'Qual a categoria de renda?', lista_campos['CATEGORIA_RENDA']
    )
    dict_respostas['PROFISSAO'] = col1_form.selectbox(
        'Qual a Ocupação?', lista_campos['PROFISSAO']
    )
    dict_respostas['TEM_FONE_CORPORATIVO'] = 1 if col1_form.selectbox(
        'Tem um telefone do trabalho?', ['Sim', 'Não']
    ) == 'Sim' else 0

    dict_respostas['RENDA_ANUAL'] = col2_form.slider(
        'Qual o salário mensal?', help='Use as setas do teclado para ajustar', 
        min_value=0, max_value=35000, step=500
    ) * 12

    dict_respostas['ANOS_EMPREGADO'] = col2_form.slider(
        'Quantos anos empregado?', help='Use as setas do teclado para ajustar', 
        min_value=0, max_value=50, step=1
    )

    dict_respostas['ANOS_DESEMPREGADO'] = col2_form.slider(
        'Quantos anos desempregado?', help='Use as setas do teclado para ajustar', 
        min_value=0, max_value=50, step=1
    )

# Expansor 2: Pessoal
with my_expander_2:
    col3_form, col4_form = st.columns(2)

    dict_respostas['TIPO_EDUCACAO'] = col3_form.selectbox(
        'Qual o Grau de Escolaridade?', lista_campos['TIPO_EDUCACAO']
    )
    dict_respostas['ESTADO_CIVIL'] = col3_form.selectbox(
        'Qual o Estado Civil?', lista_campos['ESTADO_CIVIL']
    )
    dict_respostas['TEM_CARRO'] = col3_form.selectbox(
        'Tem um Carro?', ['Sim', 'Não']
    )

    dict_respostas['TEM_FONE_FIXO'] = 1 if col4_form.selectbox(
        'Tem um telefone fixo?', ['Sim', 'Não']
    ) == 'Sim' else 0

    dict_respostas['TEM_EMAIL'] = 1 if col4_form.selectbox(
        'Tem um email?', ['Sim', 'Não']
    ) == 'Sim' else 0

    dict_respostas['ANOS_NASCIMENTO'] = col4_form.slider(
        'Qual a idade?', help='Use as setas do teclado para ajustar', 
        min_value=0, max_value=100, step=1
    )

# Expansor 3: Família
with my_expander_3:
    col5_form, col6_form = st.columns(2)

    dict_respostas['TIPO_MORADIA'] = col5_form.selectbox(
        'Qual o tipo de moradia?', lista_campos['TIPO_MORADIA']
    )
    dict_respostas['TEM_IMOVEL'] = col5_form.selectbox(
        'Tem Casa Propria?', ['Sim', 'Não']
    )

    dict_respostas['TAMANHO_FAMILIA'] = col6_form.slider(
        'Qual o tamanho da família?', help='Use as setas do teclado para ajustar', 
        min_value=1, max_value=20, step=1
    )

    dict_respostas['QTD_FILHO'] = col6_form.slider(
        'Quantos filhos?', help='Use as setas do teclado para ajustar', 
        min_value=0, max_value=20, step=1
    )

# Botão para avaliação
if st.button('Avaliar crédito'):
    if avaliar_mau(dict_respostas):
        st.error('Crédito negado')
    else:
        st.success('Crédito aprovado')



