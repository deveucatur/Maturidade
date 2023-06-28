import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Maturidade de Processos")

col1, col2, col3 = st.columns(3)

with col2:
    st.image('imagens/logoeucatur.png')

def media(lista):
    cont_numbers = 0
    soma = 0
    for a in lista:
        cont_numbers += 1
        soma += int(a)

    media_final = soma/cont_numbers

    return media_final

def indexmaior(lista):
    cont = 0
    id = 0
    for i in lista:
      cont +=1
      if i == 3:
        id = cont

    return id

def plotarRadar(data, categories, Nomes):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    # Define o limite dos eixos do gráfico
    ax.set_ylim(1, 4)
    # Define os rótulos para cada ponto dos dados
    ax.set_xticklabels(categories)
    # Cria uma lista de ângulos para cada ponto de dados
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    # Adiciona os dados ao gráfico, especificando as posições de cada ponto
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', "purple"]
    for i in range(len(data)):
        # ax.plot(angles, data[i], linewidth=2,  marker='o')
        ax.fill(angles, data[i], alpha=0.4, lw=3, ec=colors[i], fc=colors[i])
    # Define a posição dos rótulos
    ax.set_thetagrids(angles * 180 / np.pi, categories)
    ax.grid(True)
    ax.legend(Nomes, loc="upper center", bbox_to_anchor=(0.5, -0.125))
    return (fig)

col1, col2, col3 = st.columns((1,6,1))
with col2:
    st.title('Maturidade de Processos')

metricas = pd.read_excel("Dados.xlsx")
listMetric = metricas.values.tolist()

classes = list(set([x[0] for x in listMetric]))

optAval = ["1 - Falso",
           "2 - Pouco Verdadeiro",
           "3 - Amplamente Verdadeiro"]



    
with st.form("my_form"):
    macroprocesso = st.selectbox('Macroprocesso', ["Relacionamento com Cliente - Pessoas",
                                                           "Relacionamento com Cliente - Cargas",
                                                           "Administrar",
                                                           "Operar",
                                                           "Formulação Estratégica"])

    processo = st.selectbox('Processo', ["Prospectar - Pessoas",
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
    
    procedimento = st.text_input('Procedimento')
    lista_classes = []
    for a in range(len(classes)):
        st.write("---")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.title(classes[a])
        
        fatorList = set([x[1] for x in listMetric if x[0] == classes[a]])
        
        lista_fatores = []

        for fator in fatorList:
            st.subheader(f'{fator}')
            valor_fatores = []
            for alter in [x[2] for x in listMetric if x[0] == classes[a] and x[1] == fator]:
                nota = int([st.select_slider(alter, options=optAval, value=optAval[1])][0][0:1])

                #st.write(nota)

                valor_fatores.append(nota)

            lista_fatores.append([fator, indexmaior(valor_fatores)])
        lista_classes.append([classes[a], lista_fatores])
    submitted = st.form_submit_button("ENVIAR")
    if submitted:
        #st.write(lista_classes)
        st.write('---')
        col1, col2, col3 = st.columns((1.5,8,1))
        with col2:
            st.title('Apresentação das Classes')
        
        st.text(' ')

        
        #st.write(lista_classes)
        for a in range(len(classes)):
            #with col2:
            st.subheader(f'Maturidade dos Fatores ({classes[a]})')
            st.text(' ')
            #st.write(f'{lista_classes[a][0]}')
            fatoresLista = lista_classes[a][1]
            for fatores in fatoresLista:
                col1, col2 = st.columns((4,2))
                with col1:
                    st.warning(f'{fatores[0]}')
                with col2:
                    st.info(fatores[1])
    
            media_fatores = media([fatoresLista[x][1] for x in range(len(fatoresLista))]) 
            
            col1, col2 = st.columns((4,2))
            with col1:
                st.info(f'Maturidade da Classe ({classes[a]})')
            with col2:
                st.info(round(media_fatores))

st.text(' ')
st.text(' ')

st.title('Gráfico Radar')
    
notas_list = [[x[1][y][1]for y in range(len(x[1]))] for x in lista_classes]
nomes_list = [[x[1][y][0]for y in range(len(x[1]))] for x in lista_classes]

fatorLista = [lista_classes[x][1] for x in range(len(classes))]

media = []
for a in fatorLista:
    numbers = 0
    cont = 0
    for b in a:
        cont += 1
        numbers += b[1]
    media.append(numbers / cont)

nomes = []
notas = []

for lista in nomes_list:
    for nome in lista:
        nomes.append(nome)

for a in notas_list:
    for b in a:
        notas.append(b)
    
col1, col2, = st.columns(2)
        
with col1:
    st.subheader('Fatores')
    st.pyplot(plotarRadar([notas], nomes, processo))
with col2:
    st.subheader('Classes')
    st.pyplot(plotarRadar([media], classes, processo))

                



 
        

