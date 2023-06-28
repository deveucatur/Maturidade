import streamlit as st
import pandas as pd
import openpyxl
from PIL import Image

st.set_page_config(page_title="Complexidade da Posição", page_icon=Image.open('imagens/logoeucatur.png'))


col1, col2, col3 = st.columns(3)

with col2:
    st.image('imagens/logoeucatur.png')

df = pd.read_excel("metricas.xlsx")
listDados = df.values.tolist()

def obter_nome_cargo(nivel, grau, tipo_carreira):
    tabela = {
        1: {
            1: {
                "ESPECIALIZAÇÃO": "Jovem Aprendiz/Estagiário",
                "GESTÃO": "Jovem Aprendiz/Estagiário",
                "LIDERANÇA TÉCNICA": None
            },
            2: {
                "ESPECIALIZAÇÃO": "Auxiliares",
                "GESTÃO": "Auxiliares",
                "LIDERANÇA TÉCNICA": "Auxiliares"
            }
        },
        2: {
            3: {
                "ESPECIALIZAÇÃO": "Assistentes",
                "GESTÃO": "Assistentes",
                "LIDERANÇA TÉCNICA": "Assistentes"
            },
            4: {
                "ESPECIALIZAÇÃO": "Técnicos",
                "GESTÃO": "Técnicos",
                "LIDERANÇA TÉCNICA": "Técnicos"
            }
        },
        3: {
            5: {
                "ESPECIALIZAÇÃO": "Analistas/Assessores",
                "GESTÃO": "Coordenadores",
                "LIDERANÇA TÉCNICA": "Encarregados Técnicos"
            },
            6: {
                "ESPECIALIZAÇÃO": "Especialista Nível Superior",
                "GESTÃO": "Gerentes",
                "LIDERANÇA TÉCNICA": None
            }
        },
        4: {
            7: {
                "ESPECIALIZAÇÃO": "Consultores Internos",
                "GESTÃO": "Diretoria",
                "LIDERANÇA TÉCNICA": None
            },
            8: {
                "ESPECIALIZAÇÃO": None,
                "GESTÃO": "Presidência",
                "LIDERANÇA TÉCNICA": None
            }
        }
    }

    try:
        return tabela[nivel][grau][tipo_carreira]
    except KeyError:
        return None


def classifc_Nivel(soma):
    if soma < 800:
        return 1
    elif soma >= 800 and soma < 1600:
        return 2
    elif soma >= 1600 and soma < 3200:
        return 3
    elif soma >= 3200:
        return 4


def classif_Grau(soma):
    if soma < 600:
        return 1
    elif soma >= 600 and soma < 800:
        return 2
    elif soma >= 800 and soma < 1200:
        return 3
    elif soma >= 1200 and soma < 1600:
        return 4
    elif soma >= 1600 and soma < 2400:
        return 5
    elif soma >= 2400 and soma < 3200:
        return 6
    elif soma >= 3200:
        return 7


    
st.title("Complexidade da posição")
col1, col2, col3 = st.columns((0.5, 1.7, 1))
with col1:
    matricula = st.text_input("Nº Matrícula")

with col2:
    name = st.text_input("Nome Gestor de Carreira")

with col3:
    funcao = st.selectbox('Função', ["Líder de Processos", "Dono de processo", "Gestor de Processos",
                                             "Executor de Processos"])

col1, col2 = st.columns(2)
with col1:
    Unidade = st.selectbox("Unidade de negócio", ["CEEM Ariquemes",
                                                          "CEEM Boa Vista - Manaus",
                                                          "CEEM Cacoal",
                                                          "CEEM Campinas",
                                                          "CEEM Campo Grande",
                                                          "CEEM Cascavel",
                                                          "CEEM Cuiaba",
                                                          "CEEM Curitiba",
                                                          "CEEM Goiânia",
                                                          "CEEM Jí-Parana",
                                                          "CEEM Porto Alegre",
                                                          "CEEM Porto Velho",
                                                          "CEEM Pres. Prudente",
                                                          "CEEM Rio Branco",
                                                          "CEEM Rondonópolis",
                                                          "CEEM São Paulo",
                                                          "CEEM Vilhena",
                                                          "Corporativo Cascavel",
                                                          "Corporativo Jí-Parana"])
with col2:
    macroprocesso = st.selectbox('Macroprocesso', ["Relacionamento com Cliente - Pessoas",
                                                           "Relacionamento com Cliente - Cargas",
                                                           "Administrar",
                                                           "Operar",
                                                           "Formulação Estratégica"])

if macroprocesso != "Formulação Estratégica" and funcao != "Líder de Processos":
    processo = st.multiselect('Processo', ["Prospectar - Pessoas",
                                                   "Vender - Pessoas",
                                                   "Transportar - Pessoas",
                                                   "Prospectar - Cargas",
                                                   "Vender - Cargas",
                                                   "Transportar - Cargas",
                                                   "Administrar e Desenvolver Pessoas",
                                                   "Desenvolver e Potencializar Negócios",
                                                   "Administrar Recursos Financeiros",
                                                   "Administrar e Previnir o Risco Contencioso",
                                                   "Operar Ativos",
                                                   "Operar a Cadeia de Suprimentos"])
else:
    processo = ""

st.write("---")

tipo_carr = st.selectbox('Tipo de Carreira', ['ESPECIALIZAÇÃO', 'GESTÃO', 'LIDERANÇA TÉCNICA'])

escopofunç = st.text_area("Escopo da função")


fatores = set([x[0] for x in listDados])
print(fatores)

lista = []
soma = 0
for i in fatores:
    st.subheader(f'{i}')

    genre = st.radio(
        "Selecione uma opção abaixo",
        [x[2] for x in listDados if x[0] == i])

    grau = [x[1] for x in listDados if x[2] == genre]

    peso_complix = 25 * (2**(grau[0] - 1))

    soma += peso_complix

    lista.append([i, genre, grau, peso_complix])


grau_class = classif_Grau(soma)
nivel_class = classifc_Nivel(soma)
st.write("---")



if st.button("Gerar Relatório"):
    st.write("---")

    st.subheader("Relatório de Complexidade da Posição")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.text_input(f'Posição', obter_nome_cargo(nivel_class, grau_class, tipo_carr))
    with col2:
        st.text_input(f'Nivel', nivel_class)
    with col3:
        st.text_input(f'Grau', grau_class)


    st.write("---")

    st.text_area("Escopo", escopofunç)

    st.write("---")
    st.subheader("Resumo dos Fatores")

    for a in lista:
        col1, col2 = st.columns((1, 2))

        with col1:
            st.warning(f'{a[0]}')

        with col2:
            st.info(f'{a[1]}')

