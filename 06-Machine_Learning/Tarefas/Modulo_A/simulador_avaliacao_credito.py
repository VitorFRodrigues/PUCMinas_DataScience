import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador
import zipfile
import os

def descompactar_modelo(zip_path, output_dir):
    """
    Função para descompactar o arquivo .zip contendo o modelo.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Modelo descompactado em: {output_dir}")

# Definir estilo para o listbox
st.markdown(
    '<style>div[data-baseweb="select"] > div {background-color: #eee1f79e;}</style>',
    unsafe_allow_html=True
)

# Função para avaliação
def avaliar_mau(dict_respostas):
    # Verificar e descompactar o modelo, se necessário

    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
    zip_path = os.path.join(base_dir, 'Objeto', 'modelo_RandomForest.zip')
    output_dir = 'Objeto/'
    model_path = os.path.join(output_dir, 'modelo_RandomForest.joblib')

    if not os.path.exists(model_path):
        descompactar_modelo(zip_path, output_dir)

    # Carregar o modelo e as features
    modelo = load(model_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
    features_path = os.path.join(base_dir, 'Objeto', 'features.joblib')
    features = load(features_path)

    if dict_respostas['ANOS_DESEMPREGADO'] > 0:
        dict_respostas['ANOS_EMPREGADO'] = dict_respostas['ANOS_DESEMPREGADO'] * -1 

    respostas = [dict_respostas.get(col, 0) for col in features]

    df_novo_cliente = pd.DataFrame([respostas], columns=features)

    mau = modelo.predict(df_novo_cliente)[0]

    return mau

# Exibição do logotipo e título
base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
imagem_path = os.path.join(base_dir, 'img', 'bytebank_logo.png')
st.image(imagem_path)
st.title("Simulador de Avaliação de Crédito")

# Expansores para categorias
my_expander_1 = st.expander("Trabalho")
my_expander_2 = st.expander("Pessoal")
my_expander_3 = st.expander("Família")

# Dicionário para respostas
dict_respostas = {}

# Obter o caminho absoluto para o arquivo
base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
lista_campos_path = os.path.join(base_dir, 'Objeto', 'lista_campos.joblib')
lista_campos = load(lista_campos_path)

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
