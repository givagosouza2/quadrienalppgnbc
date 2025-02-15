import streamlit as st
import base64
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth


@st.cache_resource
# Função para inicializar o Firebase
def initialize_firebase():
    cred = credentials.Certificate(
        "ppgnbc-report-firebase-adminsdk-ukiu0-ceae365e20.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

# Função para tratar o arquivo de imagem


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Função para criar um gradiente de cor de fundo


def set_background_gradient():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to bottom,rgba(245, 245, 247, 0.98),rgb(7, 107, 189));
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Função para extrair o título do texto


# Ajusta a tela para formato largo e define o título da aba
st.set_page_config(layout="wide", page_title="PPGNBC-UFPA",
                   page_icon=":books:")

# Carrega imagem do banner
banner_image_path = "ppgnbc01.png"
base64_banner_image = get_base64_image(banner_image_path)

# Adiciona o CSS para estilizar o fundo e o cabeçalho
st.markdown(
    f"""
    <style>
    .header {{
        width: 100%;
        height: 300px;
        background-image: url("data:image/jpg;base64,{base64_banner_image}");
        background-size: cover;
        background-position: center;
    }}
    .stApp {{
        margin-top: 0px; /* Ajusta a margem superior para evitar sobreposição */
        padding: 0; /* Remove qualquer padding */
    }}

    /* Estiliza as abas para aumentar a fonte e deixar o texto branco */
    div[data-testid="stTabs"] button {{
        font-size: 20px !important; /* Tamanho maior */
        color: black !important; /* Texto branco */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Função principal


def main():
    # Inicializa o Firebase
    initialize_firebase()

    # Criando variáveis de banco de dados
    if 'db' not in st.session_state:
        st.session_state.db = ''

    db = firestore.client()
    st.session_state.db = db

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    # Inserindo cabeçalho com a imagem
    st.markdown(f"""<div class="header"></div>""", unsafe_allow_html=True)

    # Ajustando a cor do fundo usando a função gradiente
    set_background_gradient()

    # Criando abas com ícones e personalização da cor do texto
    tab1, tab3 = st.tabs(['🏚️ Home', '👫 Inserir dados'])

    with tab1:
        st.image('ppgnbc02.png')

    with tab3:
        docente = st.text_input('Nome do docente')
        ORCID = st.text_input('ORCID')
        lab = st.text_input('Nome do laboratório')
        
        extensao = st.text_area(
            "Indique se tem atuado em projetos de extensão, quais projetos e se há participação de discentes do PPGNBC")
        pesquisa = st.text_area(
            "Indique se tem atuado em projetos de pesquisa, quais projetos e se há participação de discentes do PPGNBC")
        sociedadescientificas = st.text_area(
            "Indique se tem atuado em Sociedades Científicas")
        colaboracao_nacional = st.text_area(
            "Indique se tem atuado em colaborações nacionais de pesquisa, quais colaborações e se há participações de discentes do PPGNBC")
        colaboracao_internacional = st.text_area(
            "Indique se tem atuado em colaborações internacionais de pesquisa, quais colaborações e se há participações de discentes do PPGNBC")
        inovacao = st.text_area(
            "Indique se tem atuado em inovação técnica/tecnológica, quais inovações e se há participações de discentes do PPGNBC")
        insercao_social = st.text_area(
            "Indique se tem atuado em ações na sociedade, quais ações e se há participações de discentes do PPGNBC")
        
        submeter = st.button('Inserir dados')

        if submeter:
            nome_da_colecao = "Dados"
            info = db.collection(nome_da_colecao)
            documentos = info.limit(1).get()
            if documentos:
                db.collection(nome_da_colecao).add({
                    'docente': docente,
                    'orcid': ORCID,
                    'lab': lab,
                    'extensao': extensao,
                    'pesquisa': pesquisa,
                    'sociedadescientificas': sociedadescientificas,
                    'colaboracaonacional': colaboracao_nacional,
                    'colaboracaointernacional': colaboracao_internacional,
                    'inovacao': inovacao,
                    'insercaosocial': insercao_social
                    })

                st.success('Dados cadastrados com sucesso')
                st.balloons()


if __name__ == "__main__":
    main()
