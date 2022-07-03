from ctypes.wintypes import RGB
import streamlit as st
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import image as image
from PIL import Image
import openpyxl
import plotly.graph_objects as go
import datetime as dt
import plotly.express as px


########################################################################
##configuração da página, texto exibido na aba e dados no item 'about'##
########################################################################

st.set_page_config(
     page_title="Agregador de pesquisas eleitorais por raça e gênero",
     page_icon="chart_with_upwards_trend",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "##### Desenvolvedor: Dirceu André Gerardi. \n **E-mail:** andregerardi3@gmail.com"
     }
 )

# import streamlit.components.v1 as components

# components.html(
#     """
#         <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button"
#         data-text="Agregador de Pesquisas eleitorais do gênero e raça - LabDados FGV Direito SP"
#         data-url="https://cebrap.org.br/teste-app/"
#         data-show-count="true">
#         data-size="Large"
#         data-hashtags="eleições2022, agregador_cebrap, python"
#         Compartilhar
#         </a>
#         <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
#     """
# )

## subtítulos do cabeçalho

##### caso queira inserir uma imagem
# image = Image.open('palacio-da-alvorada-interior-black.jpg')
# col3,col4,col5 = st.columns([.5,3,1])
# with col4:
#     st.image(image, width=800)

st.markdown("""
<h2 style='text-align: center; color:#202020;font-family:helvetica'>Agregador de pesquisas eleitorais por gênero</h2>
<br>
<h4 style='text-align: center; color:#54595F;font-family:Segoe UI, sans-serif'>Consolidação de pesquisas para as eleições presidenciais de 2022</h4>
""", unsafe_allow_html=True)

##retira o made streamlit no fim da página##
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#################
## configurações#
#################

## MÉDIA MÓVEL
m_m = 7

## MÉDIA MÓVEL 15 DIAS - ESPECIALMENTE PARA REJEIÇÃO GERAL
m_m15 = 15

### dados de tempo
end_date = dt.datetime.today() # data atual
start_date = dt.datetime(2022,1,1) # data de oito meses atras

### dados pesquisas
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_excel('banco_raca_genero_fgv.xlsx')
    return df
df = load_data()

##import image logo
@st.cache(allow_output_mutation=True)
def load_image():
    agre = Image.open('fgv-logo.jpg')
    return agre
agre = load_image()

########################################################################
#### seletor para escolher o perído do primeiro ou do segundo turno#####
########################################################################

st.markdown("---")
with st.container():
    col3,col4,col5 = st.columns([.5,1.5,.5])
    with col4:
        st.markdown("""
        <br>
        <h4 style='text-align: center; color: #ffffff; font-family:Segoe UI; background-color: #2A4B7C;'>Selecione o turno da eleição para visualizar os dados:</h4>
        """, unsafe_allow_html=True)
        options_turn = st.selectbox('',options=['--clique para selecionar--','Primeiro Turno', 'Segundo Turno'])
st.markdown("---")

########################
### primeiro turno #####
########################

if options_turn == 'Primeiro Turno':
    st.markdown(f"""
        <h2 style='text-align: center; color: #303030; font-family:tahoma; text-rendering: optimizelegibility;'>
        Primeiro Turno</h2>
        """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
        <h3 style='text-align: center; color: #ffffff; font-family:helvetica; text-rendering: optimizelegibility;background-color: #203f58;'>
        1. Intenção de voto:</h3>
        """, unsafe_allow_html=True)
    st.markdown("---")

    ############################################
    ## média movel dos candidatos por segmento##
    ############################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'>
        Resumo - intenção de voto geral por gênero e raça:</h3><br>
        """, unsafe_allow_html=True)

        int_vot_lula = st.checkbox('Lula')

        if int_vot_lula:

            ## coluna 1
            lul = Image.open('lula-oculos.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(lul,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['lul_par_1t']>1].lul_par_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['lul_amar_1t']>1].lul_amar_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            
            ## info
            st.markdown("---")

        int_vot_bolsonaro = st.checkbox('Bolsonaro')

        if int_vot_bolsonaro:

            ## coluna 1
            bol = Image.open('bolsonaro_capacete.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(bol,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['bol_amar_1t']>1].bol_amar_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            
            ## info
            st.markdown("---")

        int_vot_ciro = st.checkbox('Ciro Gomes')

        if int_vot_ciro:

            ## coluna 1
            ciro = Image.open('ciro_oculos.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(ciro,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['ciro_amar_1t']>1].ciro_amar_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            

        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado para o cálculo: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Os valores indicados no resumo correspondem a última média móvel da série temporal registrada no dia <i>{list(df.data)[-1].strftime(format='%d-%m-%Y')}</i></h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 3: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")

    #####################################################
    ## gráfico intenção de voto geral - primeiro turno###
    #####################################################


    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto geral:</h3><br>
        """, unsafe_allow_html=True)

        int_vote_med_move = st.checkbox('Selecione para visualizar o gráfico da intenção de voto geral')

        if int_vote_med_move:

            ##import image

            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df.lul_ger_1t, x=df.sigla, mode='markers', name='int_vot_geral_lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df.lul_ger_1t.rolling(m_m).mean(), x=df.sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=int(list(df.lul_ger_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df.lul_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df.bol_ger_1t, x=df.sigla, mode='markers', name='int_vot_geral_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_ger_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df.bol_ger_1t.rolling(m_m).mean(), x=df.sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=int(list(df.bol_ger_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df.bol_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df.ciro_ger_1t, x=df.sigla, mode='markers', name='int_vot_geral_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_ger_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df.ciro_ger_1t.rolling(m_m).mean(), x=df.sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=int(list(df.ciro_ger_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df.ciro_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Brancos e Nulos e não sabe e não respondeu

            fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_1t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
                                    marker=dict(
                                    size=5,
                                    color=df.bra_nul_ns_nr_ger_1t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_1t']>1].bra_nul_ns_nr_ger_1t.rolling(m_m).mean(), x=df[df['bra_nul_ns_nr_ger_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=int(list(df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -8,
                        font=dict(size=20, color="black", family="Arial"))

            # ## Brancos e Nulos

            # fig.add_trace(go.Scatter(y=df.bra_nulo_ger_1t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
            #                         marker=dict(
            #                         size=5,
            #                         color=df.bra_nulo_ger_1t, #set color equal to a variable
            #                         colorscale='Greys')))

            # fig.add_trace(go.Scatter(y=df[df['bra_nulo_ger_1t']>1].bra_nulo_ger_1t.rolling(m_m).mean(), x=df[df['bra_nulo_ger_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
            #                         line=dict(color='grey', width=2.5)))

            # fig.add_annotation(x=list(df[df['bra_nulo_ger_1t']>1].sigla)[-1], y=int(list(df[df['bra_nulo_ger_1t']>1].bra_nulo_ger_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df.bra_nulo_ger_1t.rolling(m_m).mean())[-1])}%",
            #             showarrow=True,
            #             arrowhead=1,
            #             ax = 40, ay = -8,
            #             font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Média móvel das intenções de voto de candidatos à presidência - 1º turno<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_poderdata_3", y=29,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=32,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")


            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.20,
                    sizex=0.14, sizey=0.14,
                    opacity=1,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig)

            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: *Método utilizado:* média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df.data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 3: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)
    st.markdown("---")

    
    ###################################
    ## Intenção de voto por gênero ##
    ###################################


    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por gênero:</h3><br>
        """, unsafe_allow_html=True)
        gen = st.selectbox('Selecione o gênero:',options=['--Escolha a opção--','Feminino', 'Masculino'])

    if gen == 'Feminino':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_m_1t, x=df.sigla, mode='markers', name='int_voto_lula',
                                marker=dict(
                                size=5,
                                color=df.lul_m_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean(), x=df[df['bol_m_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_m_1t']>1].sigla)[-1], y=int(list(df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_m_1t, x=df.sigla, mode='markers', name='int_voto_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_m_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean(), x=df[df['bol_m_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_m_1t']>1].sigla)[-1], y=int(list(df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro
        fig.add_trace(go.Scatter(y=df.ciro_m_1t, x=df.sigla, mode='markers', name='int_voto_ciro',
                                marker=dict(
                                size=5,
                                color=df.ciro_m_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean(), x=df[df['ciro_m_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_m_1t']>1].sigla)[-1], y=int(list(df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos e Nulos

        fig.add_trace(go.Scatter(y=df.bra_nulo_m_1t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_m_1t, #set color equal to a variable
                                colorscale='Greys')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t.rolling(m_m).mean(), x=df[df['bra_nulo_m_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                line=dict(color='grey', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_m_1t']>1].sigla)[-1], y=int(list(df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
        title=("""
        Média móvel das intenções de voto de <i>mulheres</i> por candidato à presidência - 1º turno<br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend=dict(
            yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=22,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=25,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        
        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.20,
                sizex=0.14, sizey=0.14,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais, e para o recorte de gênero, {len(df[df['lul_h_1t']>1])} pesquisas.</h7><br>
        """, unsafe_allow_html=True)

    if gen == 'Masculino':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_h_1t, x=df.sigla, mode='markers', name='int_vot_lula',
                                marker=dict(
                                size=5,
                                color=df.lul_h_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean(), x=df[df['bol_h_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_h_1t']>1].sigla)[-1], y=int(list(df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_h_1t, x=df.sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_h_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean(), x=df[df['bol_h_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_h_1t']>1].sigla)[-1], y=int(list(df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Ciro
        fig.add_trace(go.Scatter(y=df.ciro_h_1t, x=df.sigla, mode='markers', name='int_vot_ciro',
                                marker=dict(
                                size=5,
                                color=df.ciro_h_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean(), x=df[df['ciro_h_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_h_1t']>1].sigla)[-1], y=int(list(df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos e Nulos

        fig.add_trace(go.Scatter(y=df.bra_nulo_h_1t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_h_1t, #set color equal to a variable
                                colorscale='Greys')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t.rolling(m_m).mean(), x=df[df['bra_nulo_h_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                line=dict(color='grey', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_h_1t']>1].sigla)[-1], y=int(list(df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
        title=("""
        Média móvel das intenções de voto de <i>homens</i> por candidato à presidência - 1º turno<br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend=dict(
            yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=33,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=35,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.20,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais, e para o recorte de gênero, {len(df[df['lul_h_1t']>1])} pesquisas.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")

    ###################################
    ## Intenção de voto por raça ##
    ###################################

    # with st.container():
    #     st.markdown(f"""
    #     <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
    #     <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
    #     </svg> Intenção de voto por raça:</h3><br>
    #     """, unsafe_allow_html=True)
    #     raça = st.selectbox('Selecione a raça:',options=['--Escolha a opção--','Parda', 'Branca', 'Preta', 'Outras'])

    # if raça == 'Parda':

    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_par_1t']>1].lul_par_1t, x=df[df['lul_par_1t']>1].sigla, mode='markers', name='int_vot_par_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_par_1t']>1].lul_par_1t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_par_1t']>1].lul_par_1t .rolling(m_m).mean(), x=df[df['bol_par_1t']>1].sigla,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_par_1t']>1].sigla)[-1], y=int(list(df[df['lul_par_1t']>1].lul_par_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_par_1t']>1].lul_par_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_par_1t']>1].bol_par_1t, x=df[df['bol_par_1t']>1].sigla, mode='markers', name='int_vot_par_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_par_1t']>1].lul_par_1t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean(), x=df[df['bol_par_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_par_1t']>1].sigla)[-1], y=int(list(df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                    ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Ciro

    #     fig.add_trace(go.Scatter(y=df[df['ciro_par_1t']>1].ciro_par_1t, x=df[df['ciro_par_1t']>1].sigla, mode='markers', name='int_vot_par_ciro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['ciro_par_1t']>1].ciro_par_1t, #set color equal to a variable
    #                             colorscale='Greens')))

    #     fig.add_trace(go.Scatter(y=df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean(), x=df[df['ciro_par_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                             line=dict(color='seagreen', width=2.5)))

    #     fig.add_annotation(x=list(df[df['ciro_par_1t']>1].sigla)[-1], y=int(list(df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #     title=("""
    #     Média móvel das intenções de voto de <i>pardos</i> por candidato à presidência - 1º turno<br>
    #     """),
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     font=dict(family="arial",size=13),
    #                     legend=dict(
    #         yanchor="auto",
    #             y=1.15,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #     fig.add_annotation(x="mar/22_poderdata_3", y=25,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #     fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

    #     # Add image
    #     fig.add_layout_image(
    #         dict(
    #             source=agre,
    #             xref="paper", yref="paper",
    #             x=.99, y=1.20,
    #             sizex=0.12, sizey=0.12,
    #             xanchor="right", yanchor="bottom"
    #         )
    #     )

    #     st.plotly_chart(fig)

    # if raça == 'Branca':
    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_bra_1t']>1].lul_bra_1t, x=df[df['lul_bra_1t']>1].sigla, mode='markers', name='int_vot_bra_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_bra_1t']>1].lul_bra_1t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean(), x=df[df['bol_bra_1t']>1].sigla,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_bra_1t']>1].sigla)[-1], y=int(list(df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))
    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_bra_1t']>1].bol_bra_1t, x=df[df['bol_bra_1t']>1].sigla, mode='markers', name='int_vot_bra_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_bra_1t']>1].lul_bra_1t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean(), x=df[df['bol_bra_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_bra_1t']>1].sigla)[-1], y=int(list(df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))
    #     ## Ciro
    #     fig.add_trace(go.Scatter(y=df[df['ciro_bra_1t']>1].ciro_bra_1t, x=df[df['ciro_bra_1t']>1].sigla, mode='markers', name='int_vot_bra_ciro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['ciro_bra_1t']>1].ciro_bra_1t, #set color equal to a variable
    #                             colorscale='Greens')))

    #     fig.add_trace(go.Scatter(y=df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean(), x=df[df['ciro_bra_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                             line=dict(color='seagreen', width=2.5)))

    #     fig.add_annotation(x=list(df[df['ciro_bra_1t']>1].sigla)[-1], y=int(list(df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #     title=("""
    #     Média móvel das intenções de voto de <i>brancos</i> por candidato à presidência - 1º turno<br>
    #     """),
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     font=dict(family="arial",size=13),
    #                     legend=dict(
    #         yanchor="auto",
    #             y=1.15,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #     fig.add_annotation(x="mar/22_poderdata_3", y=28,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #     fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")
        
    #     # Add image
    #     fig.add_layout_image(
    #         dict(
    #             source=agre,
    #             xref="paper", yref="paper",
    #             x=.99, y=1.20,
    #             sizex=0.12, sizey=0.12,
    #             xanchor="right", yanchor="bottom"
    #         )
    #     )

    #     st.plotly_chart(fig)

    # if raça == 'Preta':
    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_pre_1t']>1].lul_pre_1t, x=df[df['lul_pre_1t']>1].sigla, mode='markers', name='int_vot_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_pre_1t']>1].lul_pre_1t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean(), x=df[df['bol_pre_1t']>1].sigla,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_pre_1t']>1].sigla)[-1], y=int(list(df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_pre_1t']>1].bol_pre_1t, x=df[df['bol_pre_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_pre_1t']>1].lul_pre_1t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean(), x=df[df['bol_pre_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_pre_1t']>1].sigla)[-1], y=int(list(df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Ciro
    #     fig.add_trace(go.Scatter(y=df[df['ciro_pre_1t']>1].ciro_pre_1t, x=df[df['ciro_pre_1t']>1].sigla, mode='markers', name='int_vot_ciro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['ciro_pre_1t']>1].ciro_pre_1t, #set color equal to a variable
    #                             colorscale='Greens')))

    #     fig.add_trace(go.Scatter(y=df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean(), x=df[df['ciro_pre_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                             line=dict(color='seagreen', width=2.5)))

    #     fig.add_annotation(x=list(df[df['ciro_pre_1t']>1].sigla)[-1], y=int(list(df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #     title=("""
    #     Média móvel das intenções de voto de <i>pretos</i> por candidato à presidência - 1º turno<br>
    #     """),
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     font=dict(family="arial",size=13),
    #                     legend=dict(
    #         yanchor="auto",
    #             y=1.15,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #     fig.add_annotation(x="mar/22_poderdata_3", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #     fig.add_annotation(x="mai/22_poderdata_2", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

      
    #     # Add image
    #     fig.add_layout_image(
    #         dict(
    #             source=agre,
    #             xref="paper", yref="paper",
    #             x=.99, y=1.19,
    #             sizex=0.14, sizey=0.14,
    #             xanchor="right", yanchor="bottom"
    #         )
    #     )

    #     st.plotly_chart(fig)

    # if raça == 'Outras':
    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_out_1t']>1].lul_out_1t, x=df[df['lul_out_1t']>1].sigla, mode='markers', name='int_vot_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_out_1t']>1].lul_out_1t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean(), x=df[df['bol_out_1t']>1].sigla,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_out_1t']>1].sigla)[-1], y=int(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_out_1t']>1].bol_out_1t, x=df[df['bol_out_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_out_1t']>1].lul_out_1t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean(), x=df[df['bol_out_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_out_1t']>1].sigla)[-1], y=int(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Ciro

    #     fig.add_trace(go.Scatter(y=df[df['ciro_out_1t']>1].ciro_out_1t, x=df[df['ciro_out_1t']>1].sigla, mode='markers', name='int_vot_ciro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['ciro_out_1t']>1].ciro_out_1t, #set color equal to a variable
    #                             colorscale='Greens')))

    #     fig.add_trace(go.Scatter(y=df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean(), x=df[df['ciro_out_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                             line=dict(color='seagreen', width=2.5)))

    #     fig.add_annotation(x=list(df[df['ciro_out_1t']>1].sigla)[-1], y=int(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #     title=("""
    #     Média móvel das intenções de voto de <i>outras</i> candidato à presidência - 1º turno<br>
    #     """),
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     font=dict(family="arial",size=13),
    #                     legend=dict(
    #         yanchor="auto",
    #             y=1.15,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #     fig.add_annotation(x="mar/22_futura", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #     fig.add_annotation(x="mai/22_futura", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

    #     # Add image
    #     fig.add_layout_image(
    #         dict(
    #             source=agre,
    #             xref="paper", yref="paper",
    #             x=.99, y=1.20,
    #             sizex=0.12, sizey=0.12,
    #             xanchor="right", yanchor="bottom"
    #         )
    #     )

    #     st.plotly_chart(fig)

    #     ## info
    # st.markdown(f"""
    # <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
    # """, unsafe_allow_html=True)
    # st.markdown("---")

    #####################################
    ### dados por instituto de pesquisa##
    #####################################

    institutos = list(set(df['nome_instituto']))
    institutos.insert(0, '--Escolha o instituto--')

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por raça, gênero e candidato segundo instituto de pesquisa: </h3><br>
        """, unsafe_allow_html=True)

        col, col1 = st.columns(2)
        with col:
            inst = st.selectbox('Selecione o instituto de pesquisa:',options=institutos)
        with col1:
            ##drop 'Parda', 'Branca', 'Preta', 'Outras', 
            raça2 = st.selectbox('Escolha a raça ou o gênero:',options=['--Selecione uma opção--','Mulheres', 'Homens'])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            # if raça2 == 'Parda':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'Pardos' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_par_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_par_1t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_par_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_par_1t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_par_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_par_1t")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça2 == 'Branca':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'Brancos' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_bra_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_bra_1t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_bra_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_bra_1t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_bra_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_bra_1t")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça2 == 'Preta':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'Pretos' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_pre_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_pre_1t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_pre_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_pre_1t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_pre_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_pre_1t")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça2 == 'Outras':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'outras' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_out_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_outras")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_out_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_outras")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_out_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_outras")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            if raça2 == 'Homens':

                df.set_index('sigla',inplace = True)

                plt.rcParams['figure.figsize'] = (12,7)
                plt.title(f"\n Intenção de voto de 'Homens' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
                plt.plot(df[df['nome_instituto']==inst].lul_h_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_homens")
                plt.plot(df[df['nome_instituto']==inst].lul_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

                plt.plot(df[df['nome_instituto']==inst].bol_h_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_homens")
                plt.plot(df[df['nome_instituto']==inst].bol_ger_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

                plt.plot(df[df['nome_instituto']==inst].ciro_h_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_homens")
                plt.plot(df[df['nome_instituto']==inst].ciro_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

                plt.style.use('ggplot')
                plt.xlabel('mês/ano e instituto de pesquisa')
                plt.xticks(rotation=80,fontsize=12)
                plt.yticks(fontsize=14)
                plt.ylabel('Intenção de voto em %')
                plt.rcParams.update({'axes.facecolor':'white'})

                plt.grid(color='black', linestyle='-', linewidth=.08)
                plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

                #axes = plt.gca()
                #axes.xaxis.grid()

                grafico = plt.savefig("grafico.png",bbox_inches='tight')

                st.pyplot(plt)

                with open(f"grafico.png", "rb") as file:
                    st.download_button(
                            label="Baixar o gráfico",
                            data=file,
                            file_name="grafico.png",
                            mime="image/png"
                            )

            if raça2 == 'Mulheres':

                df.set_index('sigla',inplace = True)

                plt.rcParams['figure.figsize'] = (12,7)
                plt.title(f"\n Intenção de voto de 'Mulheres' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
                plt.plot(df[df['nome_instituto']==inst].lul_m_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_mulheres")
                plt.plot(df[df['nome_instituto']==inst].lul_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

                plt.plot(df[df['nome_instituto']==inst].bol_m_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_mulheres")
                plt.plot(df[df['nome_instituto']==inst].bol_ger_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

                plt.plot(df[df['nome_instituto']==inst].ciro_m_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_mulheres")
                plt.plot(df[df['nome_instituto']==inst].ciro_ger_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

                plt.style.use('ggplot')
                plt.xlabel('mês/ano e instituto de pesquisa')
                plt.xticks(rotation=80,fontsize=12)
                plt.yticks(fontsize=14)
                plt.ylabel('Intenção de voto em %')
                plt.rcParams.update({'axes.facecolor':'white'})

                plt.grid(color='black', linestyle='-', linewidth=.08)
                plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

                #axes = plt.gca()
                #axes.xaxis.grid()

                grafico = plt.savefig("grafico.png",bbox_inches='tight')

                st.pyplot(plt)

                with open(f"grafico.png", "rb") as file:
                    st.download_button(
                            label="Baixar o gráfico",
                            data=file,
                            file_name="grafico.png",
                            mime="image/png"
                            )
        
        st.markdown(f"""
        <h7 style='text-align: center; color: black; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte de gênero. No entanto, nem todos os institutos divulgam tais informações. Assim, se a combinação selecionada retornar apenas os dados de intenção de voto geral, isso significa, que o instituto selecionado não disponibizou a informação em seu boletim público.</h7>
        """, unsafe_allow_html=True)
    st.markdown("---")


###########################
##rejeição primeiro turno##
###########################

    st.markdown(f"""
        <h3 style='text-align: center; color: #ffffff; font-family:helvetica; text-rendering: optimizelegibility; background-color: #203f58;'>
        2. Rejeição</h3>
        """, unsafe_allow_html=True)
    st.markdown("---")


    ####################
    ##resumo rejeição###
    ####################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #EAE6DA;'>
        Resumo - Rejeição geral e por gênero e raça segundo candidato:</h3><br>
        """, unsafe_allow_html=True)

        rej_lula = st.checkbox('Lula ')

        if rej_lula:

            ## coluna 1
            lul = Image.open('lula-oculos.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(lul,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['lul_par_rej_1t']>1].lul_par_rej_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['lul_amar_rej_1t']>1].lul_amar_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
             
            st.markdown("---")

        rej_bolsonaro = st.checkbox('Bolsonaro ')

        if rej_bolsonaro:

            bol = Image.open('bolsonaro_capacete.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(bol,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['bol_amar_rej_1t']>1].bol_amar_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            
            st.markdown("---")

        rej_ciro = st.checkbox('Ciro Gomes ')

        if rej_ciro:

            ## coluna 1
            ciro = Image.open('ciro_insta.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(ciro,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['ciro_amar_rej_1t']>1].ciro_amar_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            st.markdown("---")

        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado para o cálculo: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Os valores indicados no resumo correspondem a última média da série temporal registrada no dia <i>{list(df.data)[-1].strftime(format='%d-%m-%Y')}</i></h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 3: Para o cálculo da <i>rejeição</i> dos candidatos utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")


    ################################################
    ## gráfico da rejeição geral - primeiro turno###
    ################################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #EAE6DA;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição geral:</h3><br>
        """, unsafe_allow_html=True)

        rej_vote_med_move = st.checkbox('Selecione para visualizar o gráfico da rejeição')

        if rej_vote_med_move:

            fig = go.Figure()
            
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t, x=df[df['lul_ger_rej_1t']>1].sigla, mode='markers', name='rejeição_geral_lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean(), x=df[df['lul_ger_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean())[-1]),text=f"{int(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 25,
                        font=dict(size=20, color="black", family="Arial"))

            ## bolsonaro

            fig.add_trace(go.Scatter(y=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t, x=df[df['bol_ger_rej_1t']>1].sigla, mode='markers', name='rejeição_geral_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean(), x=df[df['bol_ger_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean())[-1]),text=f"{int(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t, x=df[df['ciro_ger_rej_1t']>1].sigla, mode='markers', name='rejeição_geral_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean(), x=df[df['ciro_ger_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_ger_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean())[-1]),text=f"{int(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -10,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Rejeição geral dos candidatos à presidência - 1º turno<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.1,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_pr_pesq", y=35,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_datafolha", y=35,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.20,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig)

            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: *Método utilizado:* média móvel de {m_m15} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 3: Para o cálculo da rejeição utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Mesmo com a aplicação da média móvel de 15 dias, o recorte temporal da rejeição geral de Ciro Gomes manteve-se oscilante. Trabalhamos com a hipótese de que a rejeição de Gomes associa-se a inclusão de concorrentes da 3a via na disputa ou de sua desistência.</h7><br>
            """, unsafe_allow_html=True)
        st.markdown("---")

    ##########################
    ## rejeição por gênero ##
    ##########################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #EAE6DA;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição por gênero:</h3><br>
        """, unsafe_allow_html=True)
        gen = st.selectbox('Selecione o gênero:',options=['--Escolha a opção--','Feminino ', 'Masculino '])

    if gen == 'Feminino ':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_m_rej_1t, x=df.sigla, mode='markers', name='int_voto_lula',
                                marker=dict(
                                size=5,
                                color=df.lul_m_rej_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean(), x=df[df['bol_m_rej_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_m_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_m_rej_1t, x=df.sigla, mode='markers', name='int_voto_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.lul_m_rej_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean(), x=df[df['bol_m_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_m_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro
        fig.add_trace(go.Scatter(y=df.ciro_m_rej_1t, x=df.sigla, mode='markers', name='int_voto_ciro',
                                marker=dict(
                                size=5,
                                color=df.ciro_m_rej_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean(), x=df[df['ciro_m_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_m_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
        title=("""
        Média móvel das intenções de voto de <i>mulheres</i> por candidato à presidência - 1º turno<br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend=dict(
            yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=22,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=25,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        
        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.20,
                sizex=0.14, sizey=0.14,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da rejeição geral utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais, e para o recorte de gênero, {len(df[df['lul_h_rej_1t']>1])} pesquisas.</h7><br>
        """, unsafe_allow_html=True)

    if gen == 'Masculino ':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_h_rej_1t, x=df.sigla, mode='markers', name='int_vot_lula',
                                marker=dict(
                                size=5,
                                color=df.lul_h_rej_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean(), x=df[df['bol_h_rej_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_h_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_h_rej_1t, x=df.sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_h_rej_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean(), x=df[df['bol_h_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_h_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Ciro
        fig.add_trace(go.Scatter(y=df.ciro_h_rej_1t, x=df.sigla, mode='markers', name='int_vot_ciro',
                                marker=dict(
                                size=5,
                                color=df.ciro_h_rej_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean(), x=df[df['ciro_h_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_h_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
        title=("""
        Média móvel das intenções de voto de <i>homens</i> por candidato à presidência - 1º turno<br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend=dict(
            yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=33,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=35,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.20,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da rejeição geral utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais, e para o recorte de gênero, {len(df[df['lul_h_rej_1t']>1])} pesquisas.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")

    ###########################
    ## rejeição por RAÇA ##      DESABILITADO, UMA VEZ QUE O N É MUITO PEQUENO.
    ###########################

    # with st.container():
    #     st.markdown(f"""
    #     <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #EAE6DA;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
    #     <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
    #     </svg> Rejeição por Raça:</h3><br>
    #     """, unsafe_allow_html=True)
        
    #     raça3 = st.selectbox('Selecione a raça:',options=[' --Escolha a opção--',' Parda', ' Branca', ' Preta', ' Outras'])

    #     if raça3 == ' Parda':

    #         fig = go.Figure()
    #         ## lula
    #         fig.add_trace(go.Scatter(y=df[df['lul_par_rej_1t']>1].lul_par_rej_1t, x=df[df['lul_par_rej_1t']>1].sigla, mode='markers', name='int_vot_par_lula',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['lul_par_rej_1t']>1].lul_par_rej_1t, #set color equal to a variable
    #                                 colorscale='peach')))

    #         fig.add_trace(go.Scatter(y=df[df['lul_par_rej_1t']>1].lul_par_rej_1t .rolling(m_m).mean(), x=df[df['bol_par_rej_1t']>1].sigla,mode='lines', name='Lula',
    #                                 line=dict(color='firebrick', width=2.5)))

    #         fig.add_annotation(x=list(df[df['lul_par_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_par_rej_1t']>1].lul_par_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_par_rej_1t']>1].lul_par_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## Bolsonaro
    #         fig.add_trace(go.Scatter(y=df[df['bol_par_rej_1t']>1].bol_par_rej_1t, x=df[df['bol_par_rej_1t']>1].sigla, mode='markers', name='int_vot_par_bolsonaro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['bol_par_rej_1t']>1].lul_par_rej_1t, #set color equal to a variable
    #                                 colorscale='ice')))

    #         fig.add_trace(go.Scatter(y=df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean(), x=df[df['bol_par_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                                 line=dict(color='skyblue', width=2.5)))

    #         fig.add_annotation(x=list(df[df['bol_par_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## Ciro

    #         fig.add_trace(go.Scatter(y=df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t, x=df[df['ciro_par_rej_1t']>1].sigla, mode='markers', name='int_vot_par_ciro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t, #set color equal to a variable
    #                                 colorscale='Greens')))

    #         fig.add_trace(go.Scatter(y=df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean(), x=df[df['ciro_par_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                                 line=dict(color='seagreen', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ciro_par_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #         title=("""
    #         Média móvel das intenções de voto de <i>pardos</i> por candidato à presidência - 1º turno<br>
    #         """),
    #                         xaxis_title='Mês, ano e instituto de pesquisa',
    #                         yaxis_title='Intenção de voto (%)',
    #                         font=dict(family="arial",size=13),
    #                         legend=dict(
    #             yanchor="auto",
    #             y=1.1,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #         fig.add_annotation(x="mar/22_poderdata_3", y=25,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #         fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #         fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

    #         # Add image
    #         fig.add_layout_image(
    #             dict(
    #                 source=agre,
    #                 xref="paper", yref="paper",
    #                 x=.99, y=1.20,
    #                 sizex=0.12, sizey=0.12,
    #                 xanchor="right", yanchor="bottom"
    #             )
    #         )

    #         st.plotly_chart(fig)

    #     if raça3 == ' Branca':
    #         fig = go.Figure()
    #         ## lula
    #         fig.add_trace(go.Scatter(y=df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t, x=df[df['lul_bra_rej_1t']>1].sigla, mode='markers', name='int_vot_bra_lula',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t, #set color equal to a variable
    #                                 colorscale='peach')))

    #         fig.add_trace(go.Scatter(y=df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean(), x=df[df['bol_bra_rej_1t']>1].sigla,mode='lines', name='Lula',
    #                                 line=dict(color='firebrick', width=2.5)))

    #         fig.add_annotation(x=list(df[df['lul_bra_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))
    #         ## Bolsonaro
    #         fig.add_trace(go.Scatter(y=df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t, x=df[df['bol_bra_rej_1t']>1].sigla, mode='markers', name='int_vot_bra_bolsonaro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['bol_bra_rej_1t']>1].lul_bra_rej_1t, #set color equal to a variable
    #                                 colorscale='ice')))

    #         fig.add_trace(go.Scatter(y=df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean(), x=df[df['bol_bra_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                                 line=dict(color='skyblue', width=2.5)))

    #         fig.add_annotation(x=list(df[df['bol_bra_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))
    #         ## Ciro
    #         fig.add_trace(go.Scatter(y=df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t, x=df[df['ciro_bra_rej_1t']>1].sigla, mode='markers', name='int_vot_bra_ciro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t, #set color equal to a variable
    #                                 colorscale='Greens')))

    #         fig.add_trace(go.Scatter(y=df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean(), x=df[df['ciro_bra_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                                 line=dict(color='seagreen', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ciro_bra_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #         title=("""
    #         Média móvel das intenções de voto de <i>brancos</i> por candidato à presidência - 1º turno<br>
    #         """),
    #                         xaxis_title='Mês, ano e instituto de pesquisa',
    #                         yaxis_title='Intenção de voto (%)',
    #                         font=dict(family="arial",size=13),
    #                         legend=dict(
    #             yanchor="auto",
    #             y=1.1,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #         fig.add_annotation(x="mar/22_poderdata_3", y=28,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #         fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #         fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")
            
    #         # Add image
    #         fig.add_layout_image(
    #             dict(
    #                 source=agre,
    #                 xref="paper", yref="paper",
    #                 x=.99, y=1.20,
    #                 sizex=0.12, sizey=0.12,
    #                 xanchor="right", yanchor="bottom"
    #             )
    #         )

    #         st.plotly_chart(fig)

    #     if raça3 == ' Preta':
    #         fig = go.Figure()
    #         ## lula
    #         fig.add_trace(go.Scatter(y=df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t, x=df[df['lul_pre_rej_1t']>1].sigla, mode='markers', name='int_vot_lula',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t, #set color equal to a variable
    #                                 colorscale='peach')))

    #         fig.add_trace(go.Scatter(y=df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean(), x=df[df['bol_pre_rej_1t']>1].sigla,mode='lines', name='Lula',
    #                                 line=dict(color='firebrick', width=2.5)))

    #         fig.add_annotation(x=list(df[df['lul_pre_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## Bolsonaro
    #         fig.add_trace(go.Scatter(y=df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t, x=df[df['bol_pre_rej_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['bol_pre_rej_1t']>1].lul_pre_rej_1t, #set color equal to a variable
    #                                 colorscale='ice')))

    #         fig.add_trace(go.Scatter(y=df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean(), x=df[df['bol_pre_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                                 line=dict(color='skyblue', width=2.5)))

    #         fig.add_annotation(x=list(df[df['bol_pre_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## Ciro
    #         fig.add_trace(go.Scatter(y=df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t, x=df[df['ciro_pre_rej_1t']>1].sigla, mode='markers', name='int_vot_ciro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t, #set color equal to a variable
    #                                 colorscale='Greens')))

    #         fig.add_trace(go.Scatter(y=df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean(), x=df[df['ciro_pre_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                                 line=dict(color='seagreen', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ciro_pre_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #         title=("""
    #         Média móvel das intenções de voto de <i>pretos</i> por candidato à presidência - 1º turno<br>
    #         """),
    #                         xaxis_title='Mês, ano e instituto de pesquisa',
    #                         yaxis_title='Intenção de voto (%)',
    #                         font=dict(family="arial",size=13),
    #                         legend=dict(
    #             yanchor="auto",
    #             y=1.1,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #         fig.add_annotation(x="mar/22_poderdata_3", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #         fig.add_annotation(x="mai/22_poderdata_2", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #         fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        
    #         # Add image
    #         fig.add_layout_image(
    #             dict(
    #                 source=agre,
    #                 xref="paper", yref="paper",
    #                 x=.99, y=1.19,
    #                 sizex=0.14, sizey=0.14,
    #                 xanchor="right", yanchor="bottom"
    #             )
    #         )

    #         st.plotly_chart(fig)

    #     if raça3 == ' Outras':
    #         fig = go.Figure()
    #         ## lula
    #         fig.add_trace(go.Scatter(y=df[df['lul_out_rej_1t']>1].lul_out_rej_1t, x=df[df['lul_out_rej_1t']>1].sigla, mode='markers', name='int_vot_lula',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['lul_out_rej_1t']>1].lul_out_rej_1t, #set color equal to a variable
    #                                 colorscale='peach')))

    #         fig.add_trace(go.Scatter(y=df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean(), x=df[df['bol_out_rej_1t']>1].sigla,mode='lines', name='Lula',
    #                                 line=dict(color='firebrick', width=2.5)))

    #         fig.add_annotation(x=list(df[df['lul_out_rej_1t']>1].sigla)[-1], y=int(list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## Bolsonaro
    #         fig.add_trace(go.Scatter(y=df[df['bol_out_rej_1t']>1].bol_out_rej_1t, x=df[df['bol_out_rej_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['bol_out_rej_1t']>1].lul_out_rej_1t, #set color equal to a variable
    #                                 colorscale='ice')))

    #         fig.add_trace(go.Scatter(y=df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean(), x=df[df['bol_out_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
    #                                 line=dict(color='skyblue', width=2.5)))

    #         fig.add_annotation(x=list(df[df['bol_out_rej_1t']>1].sigla)[-1], y=int(list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## Ciro

    #         fig.add_trace(go.Scatter(y=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t, x=df[df['ciro_out_rej_1t']>1].sigla, mode='markers', name='int_vot_ciro',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t, #set color equal to a variable
    #                                 colorscale='Greens')))

    #         fig.add_trace(go.Scatter(y=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean(), x=df[df['ciro_out_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
    #                                 line=dict(color='seagreen', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ciro_out_rej_1t']>1].sigla)[-1], y=int(list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #         title=("""
    #         Média móvel das intenções de voto de <i>outras</i> candidato à presidência - 1º turno<br>
    #         """),
    #                         xaxis_title='Mês, ano e instituto de pesquisa',
    #                         yaxis_title='Intenção de voto (%)',
    #                         font=dict(family="arial",size=13),
    #                         legend=dict(
    #             yanchor="auto",
    #             y=1.1,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #         fig.add_annotation(x="mar/22_futura", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #         fig.add_annotation(x="mai/22_futura", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #         fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

    #         # Add image
    #         fig.add_layout_image(
    #             dict(
    #                 source=agre,
    #                 xref="paper", yref="paper",
    #                 x=.99, y=1.20,
    #                 sizex=0.12, sizey=0.12,
    #                 xanchor="right", yanchor="bottom"
    #             )
    #         )

    #         st.plotly_chart(fig)


    #####################################
    ### dados por instituto de pesquisa##
    #####################################

    institutos = list(set(df['nome_instituto']))
    institutos.insert(0, '--Escolha o instituto--')

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #EAE6DA;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição por gênero e candidato segundo instituto de pesquisa: </h3><br>
        """, unsafe_allow_html=True)

        col, col1 = st.columns(2)
        with col:
            inst = st.selectbox(' Selecione o instituto de pesquisa: ',options=institutos)
        with col1:
            ##drop ' Parda ', ' Branca ', ' Preta ', ' Outras ', 
            raça4 = st.selectbox('Escolha o gênero:',options=[' --Selecione uma opção-- ',' Mulheres ', ' Homens '])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:

            # if raça4 == ' Parda ':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Rejeição de 'Pardos' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_par_rej_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_par_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_par_rej_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_par_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_rej_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_par_rej_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_par_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça4 == ' Branca ':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Rejeição de 'Brancos' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_bra_rej_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_bra_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_bra_rej_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_bra_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_rej_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_bra_rej_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_bra_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça4 == ' Preta ':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Rejeição de 'Pretos' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_pre_rej_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_pre_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_pre_rej_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_pre_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_rej_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_pre_rej_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_pre_rej_1t")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça4 == ' Outras ':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Rejeição de 'outras' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_out_rej_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_outras")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_out_rej_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_outras")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_rej_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.plot(df[df['nome_instituto']==inst].ciro_out_rej_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_outras")
            #     plt.plot(df[df['nome_instituto']==inst].ciro_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            if raça4 == ' Homens ':

                df.set_index('sigla',inplace = True)

                plt.rcParams['figure.figsize'] = (12,7)
                plt.title(f"\n Rejeição de 'Homens' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
                plt.plot(df[df['nome_instituto']==inst].lul_h_rej_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_homens")
                plt.plot(df[df['nome_instituto']==inst].lul_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

                plt.plot(df[df['nome_instituto']==inst].bol_h_rej_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_homens")
                plt.plot(df[df['nome_instituto']==inst].bol_ger_rej_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

                plt.plot(df[df['nome_instituto']==inst].ciro_h_rej_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_homens")
                plt.plot(df[df['nome_instituto']==inst].ciro_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

                plt.style.use('ggplot')
                plt.xlabel('mês/ano e instituto de pesquisa')
                plt.xticks(rotation=80,fontsize=12)
                plt.yticks(fontsize=14)
                plt.ylabel('Intenção de voto em %')
                plt.rcParams.update({'axes.facecolor':'white'})

                plt.grid(color='black', linestyle='-', linewidth=.08)
                plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

                #axes = plt.gca()
                #axes.xaxis.grid()

                grafico = plt.savefig("grafico.png",bbox_inches='tight')

                st.pyplot(plt)

                with open(f"grafico.png", "rb") as file:
                    st.download_button(
                            label="Baixar o gráfico",
                            data=file,
                            file_name="grafico.png",
                            mime="image/png"
                            )

            if raça4 == ' Mulheres ':

                df.set_index('sigla',inplace = True)

                plt.rcParams['figure.figsize'] = (12,7)
                plt.title(f"\n Rejeição de 'Mulheres' à presidente - {inst.title()} 1º turno" + "\n", fontdict={'fontsize':18})
                plt.plot(df[df['nome_instituto']==inst].lul_m_rej_1t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_mulheres")
                plt.plot(df[df['nome_instituto']==inst].lul_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

                plt.plot(df[df['nome_instituto']==inst].bol_m_rej_1t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_mulheres")
                plt.plot(df[df['nome_instituto']==inst].bol_ger_rej_1t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

                plt.plot(df[df['nome_instituto']==inst].ciro_m_rej_1t, data=df, marker='.', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=3, label="ciro_mulheres")
                plt.plot(df[df['nome_instituto']==inst].ciro_ger_rej_1t, data=df, marker='.',linestyle='dashed', markerfacecolor='seagreen', markersize=8, color='seagreen', linewidth=1, label="ciro_geral")

                plt.style.use('ggplot')
                plt.xlabel('mês/ano e instituto de pesquisa')
                plt.xticks(rotation=80,fontsize=12)
                plt.yticks(fontsize=14)
                plt.ylabel('Intenção de voto em %')
                plt.rcParams.update({'axes.facecolor':'white'})

                plt.grid(color='black', linestyle='-', linewidth=.08)
                plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

                #axes = plt.gca()
                #axes.xaxis.grid()

                grafico = plt.savefig("grafico.png",bbox_inches='tight')

                st.pyplot(plt)

                with open(f"grafico.png", "rb") as file:
                    st.download_button(
                            label="Baixar o gráfico",
                            data=file,
                            file_name="grafico.png",
                            mime="image/png"
                            )
        
        st.markdown(f"""
        <h7 style='text-align: center; color: black; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte de rejição por raça e gênero. No entanto, nem todos os institutos coletam tais informações a partir da amostra de racial, sendo mais abundantes os dados sobre gênero.</h7>
        """, unsafe_allow_html=True)
    st.markdown("---")



#############################################################################################################################
                                                        ### segundo turno ######
#############################################################################################################################

if options_turn == 'Segundo Turno':

    st.markdown(f"""
        <h2 style='text-align: center; color: #303030; font-family:tahoma; text-rendering: optimizelegibility'>Segundo Turno</h2>
        <br>
        """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
        <h3 style='text-align: center; color: #ffffff; font-family:helvetica; text-rendering: optimizelegibility;background-color: #203f58;'>
        1. Intenção de voto:</h3>
        """, unsafe_allow_html=True)
    st.markdown("---")


    ##################
    ##resumo#########
    #################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'>
        Resumo - intenção de voto por candidato</h3> \n
        <br>""", unsafe_allow_html=True)

        int_vot_lula2 = st.checkbox('Lula')

        if int_vot_lula2:

            ## coluna 1
            lul = Image.open('lula-oculos.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(lul,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['lul_par_2t']>1].lul_par_2t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['lul_bra_2t']>1].lul_bra_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['lul_pre_2t']>1].lul_pre_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['lul_amar_2t']>1].lul_amar_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1],1),1)}")
            
            ## info
            st.markdown("---")

        int_vot_bolsonaro2 = st.checkbox('Bolsonaro')

        if int_vot_bolsonaro2:

            ## coluna 1
            bol = Image.open('bolsonaro_capacete.jpg')
            col0,col, col1, col2 = st.columns(4)
            col0.image(bol,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Homem", value=f"{round(list(df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Mulher", value=f"{round(list(df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Pardo", value=f"{round(list(df[df['bol_par_2t']>1].bol_par_2t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1),1)}")

            # ## coluna 2
            # col5, col6, col7, col8, col9 = st.columns(5)
            # col5.metric(label="",value="")
            # col6.metric(label="Branco", value=f"{round(list(df[df['bol_bra_2t']>1].bol_bra_2t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1],1)}")
            # col7.metric(label="Preto", value=f"{round(list(df[df['bol_pre_2t']>1].bol_pre_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1),1)}")
            # col8.metric(label="Amarelo", value=f"{round(list(df[df['bol_amar_2t']>1].bol_amar_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1],1),1)}")
            # col9.metric(label="Outros", value=f"{round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1],1),1)}")
            
            ## info
            st.markdown("---")

        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7> \n
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Os valores indicados no resumo correspondem a última média da série temporal registrada no dia *{list(df.data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 3: Para o cálculo do resumo da média móvel das intenções de voto geral ao segundo turno utilizamos {len(df[df['lul_ger_2t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)
    st.markdown("---")


    ################################
    ## Média movel segundo turno###
    ################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto geral</h3>
        <br>""", unsafe_allow_html=True)

        int_vote_med_move_2t = st.checkbox('Clique para visualizar')

        if int_vote_med_move_2t:

            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df.lul_ger_2t, x=df.sigla, mode='markers', name='int_vot_geral_lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_2t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_2t']>1].sigla)[-1], y=int(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                    ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df.bol_ger_2t, x=df.sigla, mode='markers', name='int_vot_geral_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_2t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_2t']>1].sigla)[-1], y=int(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                    ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            # ## Brancos e Nulos e não sabe e não respondeu

            fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_2t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
                                    marker=dict(
                                    size=5,
                                    color=df.bra_nul_ns_nr_ger_2t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean(), x=df[df['bra_nul_ns_nr_ger_2t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df[df['bra_nul_ns_nr_ger_2t']>1].sigla)[-1], y=int(list(df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -8,
                        font=dict(size=20, color="black", family="Arial"))

            ## Brancos e Nulos

            # fig.add_trace(go.Scatter(y=df.bra_nulo_ger_2t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
            #                         marker=dict(
            #                         size=5,
            #                         color=df.bra_nulo_ger_2t, #set color equal to a variable
            #                         colorscale='Greys')))

            # fig.add_trace(go.Scatter(y=df[df['bra_nulo_ger_2t']>1].bra_nulo_ger_2t.rolling(m_m).mean(), x=df[df['bra_nulo_ger_2t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
            #                         line=dict(color='grey', width=2.5)))

            # fig.add_annotation(x=list(df[df['bra_nulo_ger_2t']>1].sigla)[-1], y=int(list(df[df['bra_nulo_ger_2t']>1].bra_nulo_ger_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bra_nulo_ger_2t']>1].bra_nulo_ger_2t.rolling(m_m).mean())[-1])}%",
            #             showarrow=True,
            #             arrowhead=1,
            #             ax = 40, ay = -8,
            #             font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            Média móvel das intenções de voto de geral por candidato à presidência - 2º turno<br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.1,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_poderdata_3", y=30,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=30,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")
            fig.update_yaxes(range=[0,70])

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.20,
                    sizex=0.14, sizey=0.14,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig)
            st.markdown(f"""
            <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: *Método utilizado:* média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df.data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 3: Para o cálculo da média móvel da intenção de voto geral ao segundo turno utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>

            """, unsafe_allow_html=True)
    
    st.markdown("---")

    ############################
    ### intenção de voto média##
    ############################

    ###################################
    ## Intenção de voto por gênero ##
    ###################################


    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por gênero:</h3><br>
        """, unsafe_allow_html=True)
        gen5 = st.selectbox('Selecione o gênero:',options=[' --Escolha a opção--',' Feminino', ' Masculino'])

    if gen5 == ' Feminino':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_m_2t, x=df.sigla, mode='markers', name='int_voto_lula',
                                marker=dict(
                                size=5,
                                color=df.lul_m_2t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean(), x=df[df['bol_m_2t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_m_2t']>1].sigla)[-1], y=int(list(df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_m_2t, x=df.sigla, mode='markers', name='int_voto_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_m_2t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean(), x=df[df['bol_m_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_m_2t']>1].sigla)[-1], y=int(list(df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
        title=("""
        Média móvel das intenções de voto de <i>mulheres</i> por candidato à presidência - 2º turno<br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend=dict(
            yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=22,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=25,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        
        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.20,
                sizex=0.14, sizey=0.14,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_2t']>1])} pesquisas eleitorais, e para o recorte de gênero, {len(df[df['lul_h_2t']>1])} pesquisas.</h7><br>
        """, unsafe_allow_html=True)

    if gen5 == ' Masculino':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_h_2t, x=df.sigla, mode='markers', name='int_vot_lula',
                                marker=dict(
                                size=5,
                                color=df.lul_h_2t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean(), x=df[df['bol_h_2t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_h_2t']>1].sigla)[-1], y=int(list(df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_h_2t, x=df.sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_h_2t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean(), x=df[df['bol_h_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_h_2t']>1].sigla)[-1], y=int(list(df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean())[-1]),text=f"{int(list(df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
        title=("""
        Média móvel das intenções de voto de <i>homens</i> por candidato à presidência - 2º turno<br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend=dict(
            yanchor="auto",
                y=1.15,
                xanchor="auto",
                x=0.5,
                orientation="h",
                font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=33,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=35,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.20,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_2t']>1])} pesquisas eleitorais, e para o recorte de gênero, {len(df[df['lul_h_2t']>1])} pesquisas.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")

    #####################################
    ### dados por instituto de pesquisa##
    #####################################

    institutos = list(set(df['nome_instituto']))
    institutos.insert(0, '--Escolha o instituto--')

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por gênero e candidato segundo instituto de pesquisa: </h3><br>
        """, unsafe_allow_html=True)

        col, col1 = st.columns(2)
        with col:
            inst = st.selectbox('Selecione o instituto de pesquisa:',options=institutos)
        with col1:
            ## drop'  Parda', '  Branca', '  Preta', '  Outras', 
            raça6 = st.selectbox('Escolha o gênero:',options=['  --Selecione uma opção--  ','  Mulheres', '  Homens'])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            # if raça6 == '  Parda':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'Pardos' à presidente - {inst.title()} 2º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_par_2t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_par_2t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_2t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_par_2t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_par_2t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_2t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça6 == '  Branca':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'Brancos' à presidente - {inst.title()} 2º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_bra_2t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_bra_2t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_2t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_bra_2t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_bra_2t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_2t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça6 == '  Preta':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'Pretos' à presidente - {inst.title()} 2º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_pre_2t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_pre_2t")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_2t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_pre_2t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_pre_2t")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_2t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            # if raça6 == '  Outras':

            #     df.set_index('sigla',inplace = True)

            #     plt.rcParams['figure.figsize'] = (12,7)
            #     plt.title(f"\n Intenção de voto de 'outras' à presidente - {inst.title()} 2º turno" + "\n", fontdict={'fontsize':18})
            #     plt.plot(df[df['nome_instituto']==inst].lul_out_2t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_outras")
            #     plt.plot(df[df['nome_instituto']==inst].lul_ger_2t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

            #     plt.plot(df[df['nome_instituto']==inst].bol_out_2t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_outras")
            #     plt.plot(df[df['nome_instituto']==inst].bol_ger_2t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

            #     plt.style.use('ggplot')
            #     plt.xlabel('mês/ano e instituto de pesquisa')
            #     plt.xticks(rotation=80,fontsize=12)
            #     plt.yticks(fontsize=14)
            #     plt.ylabel('Intenção de voto em %')
            #     plt.rcParams.update({'axes.facecolor':'white'})

            #     plt.grid(color='black', linestyle='-', linewidth=.08)
            #     plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

            #     #axes = plt.gca()
            #     #axes.xaxis.grid()

            #     grafico = plt.savefig("grafico.png",bbox_inches='tight')

            #     st.pyplot(plt)

            #     with open(f"grafico.png", "rb") as file:
            #         st.download_button(
            #                 label="Baixar o gráfico",
            #                 data=file,
            #                 file_name="grafico.png",
            #                 mime="image/png"
            #                 )

            if raça6 == '  Homens':

                df.set_index('sigla',inplace = True)

                plt.rcParams['figure.figsize'] = (12,7)
                plt.title(f"\n Intenção de voto de 'Homens' à presidente - {inst.title()} 2º turno" + "\n", fontdict={'fontsize':18})
                plt.plot(df[df['nome_instituto']==inst].lul_h_2t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_homens")
                plt.plot(df[df['nome_instituto']==inst].lul_ger_2t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

                plt.plot(df[df['nome_instituto']==inst].bol_h_2t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_homens")
                plt.plot(df[df['nome_instituto']==inst].bol_ger_2t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

                plt.style.use('ggplot')
                plt.xlabel('mês/ano e instituto de pesquisa')
                plt.xticks(rotation=80,fontsize=12)
                plt.yticks(fontsize=14)
                plt.ylabel('Intenção de voto em %')
                plt.rcParams.update({'axes.facecolor':'white'})

                plt.grid(color='black', linestyle='-', linewidth=.08)
                plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

                #axes = plt.gca()
                #axes.xaxis.grid()

                grafico = plt.savefig("grafico.png",bbox_inches='tight')

                st.pyplot(plt)

                with open(f"grafico.png", "rb") as file:
                    st.download_button(
                            label="Baixar o gráfico",
                            data=file,
                            file_name="grafico.png",
                            mime="image/png"
                            )

            if raça6 == '  Mulheres':

                df.set_index('sigla',inplace = True)

                plt.rcParams['figure.figsize'] = (12,7)
                plt.title(f"\n Intenção de voto de 'Mulheres' à presidente - {inst.title()} 2º turno" + "\n", fontdict={'fontsize':18})
                plt.plot(df[df['nome_instituto']==inst].lul_m_2t, data=df, marker='.', markerfacecolor='firebrick', markersize=10, color='red', linewidth=3,alpha=0.6, label="lul_mulheres")
                plt.plot(df[df['nome_instituto']==inst].lul_ger_2t, data=df, marker='.',linestyle='dashed', markerfacecolor='firebrick', markersize=5, color='red', linewidth=1,alpha=0.6, label="lula_geral")

                plt.plot(df[df['nome_instituto']==inst].bol_m_2t, data=df, marker='*', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=3, label="bol_mulheres")
                plt.plot(df[df['nome_instituto']==inst].bol_ger_2t, data=df, marker='*',linestyle='dashed', markerfacecolor='skyblue', markersize=8, color='skyblue', linewidth=1, label="bolsonaro_geral")

                plt.style.use('ggplot')
                plt.xlabel('mês/ano e instituto de pesquisa')
                plt.xticks(rotation=80,fontsize=12)
                plt.yticks(fontsize=14)
                plt.ylabel('Intenção de voto em %')
                plt.rcParams.update({'axes.facecolor':'white'})

                plt.grid(color='black', linestyle='-', linewidth=.08)
                plt.legend(fontsize=9, loc='best',ncol=3, borderaxespad=0.)

                #axes = plt.gca()
                #axes.xaxis.grid()

                grafico = plt.savefig("grafico.png",bbox_inches='tight')

                st.pyplot(plt)

                with open(f"grafico.png", "rb") as file:
                    st.download_button(
                            label="Baixar o gráfico",
                            data=file,
                            file_name="grafico.png",
                            mime="image/png"
                            )
        
        st.markdown(f"""
        <h7 style='text-align: center; color: black; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte de gênero. No entanto, nem todos os institutos coletam tais informações. Assim, se a combinação selecionada retornar apenas os dados de intenção de voto geral, isso significa, que o instituto selecionado não coletou a informação.</h7>
        """, unsafe_allow_html=True)
    st.markdown("---")
    
###############################################################################
## importa e plota o quadro com a lista de pesquisas utilizadas pelo agregador##
################################################################################

with st.container():
    col3,col4,col5 = st.columns([.5,4,.5])
    with col4:
        st.markdown("""
        <br>
        <h4 style='text-align: center; color: #303030;font-family:Segoe UI;background-color: #F5DF4D;'><b>Informações sobre o agregador:<b></h4><br>
        """, unsafe_allow_html=True)

        ### primeiro expander, da metodologia
        expander = st.expander("Entenda como o agregador foi construído")
        expander.markdown(f"""
        <!DOCTYPE html>
        <html>
        <body>

        <p style='text-align: center; font-family:Segoe UI;'><b>Explicação:</b></p>

        <p style='text-align: justify; font-family:Segoe UI;'>1. O banco de dados é atualizado constantemente. No momento, ele contém informações de {len(df)} pesquisas eleitorais;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>2. Os institutos de pesquisa consultados são: { ', '.join(set(df['nome_instituto'].T)).title()};</p>
        <p style='text-align: justify; font-family:Segoe UI;'>3. O agregador de pesquisas por gênero e raça compila dados dos levantamentos realizados pelos institutos. Não nos responsabilizamos pelas amostras ou técnicas;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>4. Para a composição do banco de dados são consideradas apenas pesquisas nacionais, bem como informações dos três principais candidatos do 1º turno das eleições presidenciais: Lula, Bolsonaro e Ciro Gomes, e de Lula e Bolsonaro, no 2º turno. Levando em conta o recorte de gênero e por raça, a partir de tais pesquisas, coletamos as intenção de voto dos candidatos nos dois turnos, assim como a rejeição;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>5. O percentual de <i>rejeição</i> dos candidatos obtivemos por meio da resposta de eleitores que declaram "não votar de jeito nenhum” em determinado candidato;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>6. O percentual de <i>reprovação da administração</i> do Presidente Jair Bolsonaro foi obtido a partir da soma da respostas "ruim" e "péssimo" à questão que avalia a satisfação dos eleitores para com a administração do mandatário: "a administração do Presidente Jair Bolsonaro está sendo ótima, boa, regular, ruim ou péssima?";</p> 
        <p style='text-align: justify; font-family:Segoe UI;'>7. Os institutos de pesquisa não incluem dados do recorte racial em todas as pesquisas realizadas por motivos internos. Portanto, a coleta de tais informações é inconstante, visto que nem sempre está disponível;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>8. Devido a irregularidade na coleta e ao tamanho da amostra, dados referentes a raças demograficamente minoritárias tal como amarelos e indígenas, entre outras mais, apresentam do ponto de vista estatístico distorções severas. Assim, quando os dados permitem, decidiu-se pela sua inclusão na categoria "outros";</p>
        <p style='text-align: justify; font-family:Segoe UI;'>9. Vale destacar que os dados censitários, principais referências para a construção da amostragem das pesquisas, estão defasados. Os valores de amostragem variam conforme os critérios próprios de cada instituto de pesquisa. Os institutos utilizam dados o IBGE de 2010, da PNAD de 2021 e 2022 e também do TSE. Os dados das amostras por raça nem sempre constam nos documentos divulgados pelas agências e também não são registrados no sistema <a href="https://www.tse.jus.br/eleicoes/pesquisa-eleitorais/consulta-as-pesquisas-registradas"><b>PesqeEle</b></a>, do TSE, uma vez que não é um dado obrigatório, segundo o artigo 33 da <a href="https://www.tse.jus.br/legislacao/codigo-eleitoral/lei-das-eleicoes/sumario-lei-das-eleicoes-lei-nb0-9.504-de-30-de-setembro-de-1997">Lei nº 9.504/1997.</a> Para termos uma noção do universo amostrado pelos institutos: Em relação a amostra de gênero dos candidatos, os <i>homens</i> variaram entre {int(df['am_h'].agg('min'))}% e {int(df['am_h'].agg('max'))}% e as <i>mulheres</i> entre {int(df['am_m'].agg('min'))}% e {int(df['am_m'].agg('max'))}%. Em relação ao recorte racial, a amostra dos <i>pardos</i> variou entre {int(df['am_par'].agg('min'))}% e {int(df['am_par'].agg('max'))}%; <i>brancos</i>, de {int(df['am_bra'].agg('min'))}% a {int(df['am_bra'].agg('max'))}%; <i>pretos</i>, de {int(df['am_pre'].agg('min'))}% a {int(df['am_pre'].agg('max'))}%; <i>amarelos</i> entre {int(df['am_amar'].agg('min'))}% e {int(df['am_amar'].agg('max'))}%; <i>indígenas</i>, de {int(df['am_ind'].agg('min'))}% e {int(df['am_ind'].agg('max'))}% e a categoria <i>outros</i> variou de {int(df['am_out'].agg('min'))}% a {int(df['am_out'].agg('max'))}%.;</p> 
        <p style='text-align: justify; font-family:Segoe UI;'>10. Em relação às pesquisas, no levantamento de dados para o agregador, consideramos a última data quando os entrevistadores colheram as respostas e não a data da divulgação da pesquisa, que por interesses diversos, podem ser adiadas por semanas ou não publicadas;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>11. Partindo da data da última coleta das pesquisas calculou-se a média móvel de diversas variáveis correspondendo à {m_m} dias;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>12. Para obter a média móvel utilizamos dados de uma série temporal e aplicamos o seguinte código Python <code>rolling().mean()</code>. Uma explicação detalhada da utilização deste código pode ser <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html">vista aqui</a>;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>13. Ao calcular a média móvel, os {m_m} primeiros resultados são omitidos dos gráficos. O objetivo principal da aplicação deste método é reduzir as oscilações no intuito de deixar as linhas dos gráficos mais fluídas. Exitem outras outras técnicas estatíticas para a redução do ruído dos dados da série temporal, tais como <i>weighted moving average, kernel smoother</i>, entre outras;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>14. O resumo das médias móveis apresentado no primeiro e segundo turnos considera e apresenta o último valor da média obtida para cada candidato. O dado é atualizado automaticamente à medida que novas pesquisas são inseridas no banco de dados;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>15. Para deixar os gráficos limpos optou-se por não inserir a margem de erro na linha da média móvel, dado que nos recortes por gênero e raça variam de 2% à 8,5%, segundo os institutos. Uma lista com as informações amostrais de cada pesquisa, incluíndo a margem de erro, poderá ser obtida na aba "pesquisas eleitorais utilizadas";</p>
        <p style='text-align: justify; font-family:Segoe UI;'>16. As imagens dos candidatos que utilizamos provêm de fontes externas: <a href="https://oglobo.globo.com/epoca/o-que-dizem-os-autores-dos-programas-dos-presidenciaveis-sobre-combate-as-mudancas-climaticas-23128520">Ciro Gomes</a>, <a href="https://www.dw.com/pt-br/o-brasil-na-imprensa-alem%C3%A3-29-05/a-48968730/">Lula</a>, <a href="https://www.poder360.com.br/poderdata/poderdata-lula-tem-50-contra-40-de-bolsonaro-no-2o-turno/">Bolsonaro</a>.</p>

        </body>
        </html>
        """,unsafe_allow_html=True)

        ### lista de pesquisas
        expander3 = st.expander("Verifique as pesquisas eleitorais utilizadas")
        expander3.write("""#### Lista de pesquisas""")
        lista = df[['nome_instituto', 'data', 'registro_tse','entrevistados', 'margem_erro', 'confiança', 'tipo_coleta']].fillna(0).astype({'nome_instituto': 'str', 'data': 'datetime64', 'registro_tse': 'str', 'entrevistados':'int','margem_erro':'str','confiança':'int', 'tipo_coleta':'str'})
        expander3.dataframe(lista)

        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8-sig')

        csv = convert_df(lista)

        expander3.download_button(
            label="Baixe a lista em CSV",
            data=csv,
            file_name='lista.csv',
            mime='text/csv',
        )
        expander3.caption('*Fontes*: TSE e Institutos de Pesquisa')

with st.container():
    col,col1,col2,col3, col4 = st.columns([.5,1.3,1.3,1.3,.5])
    with col1:
        expander4 = st.expander('Estatíticas do agregador')
        expander4.markdown(f"""<br>
            <br>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Abrangencia das pesquisas:</h6> <p style='text-align: center';>Nacional</p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Institutos analisados:</h6> <p style='text-align: center';>{', '.join(set(df['nome_instituto'].T)).title()}</p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Método de coleta das pesquisas:</h6><p style='text-align: center';>
                Telefone: {df[df['tipo_coleta']=='telefone'].tipo_coleta.value_counts()[0]}
                <br>Presencial: {df[df['tipo_coleta']=='presencial'].tipo_coleta.value_counts()[0]}</p>
            <h6 style='text-align: center; color:#0b437e;font-family:Segoe UI;'>Contador de pesquisas para dados gerais:</h6> 
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            1º turno: {len(df[df['lul_ger_1t']>=1])}<br>
            2º turno: {len(df[df['lul_ger_2t']>=1])}</p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Contador de pesquisas com perguntas sobre gênero e raça:</h6> 
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            1º turno<br>
            <p style='text-align: center';>Gênero: {len(df[df['lul_h_1t']>=1])}  |  Raça: {len(df[df['lul_bra_1t']>=1])}<br>
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            2º turno<br>
            <p style='text-align: center';>Gênero: {len(df[df['lul_h_2t']>=1])}  |  Raça: {len(df[df['lul_bra_2t']>=1])}<br>
            </p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Total de pesquisas com amostra sobre gênero e raça:</h6><p style='text-align: center';>
            Pardo: {len(df[df['lul_par_1t']>=1])}
            <br>Branco: {len(df[df['lul_bra_1t']>=1])}
            <br>Preto: {len(df[df['lul_pre_1t']>=1])}
            <br>Amarelo: {len(df[df['lul_amar_1t']>=1])}
            <br>Indígena: {len(df[df['lul_ind_1t']>=1])}
            <br>Outras: {len(df[df['lul_out_1t']>=1])}
            <br>
            <br>Homem: {len(df[df['lul_h_1t']>=1])}
            <br>Mulher: {len(df[df['lul_m_1t']>=1])}
            </p>
        """, unsafe_allow_html=True)

        ### Como citar o agregador ####
    with col2:
        expander2 = st.expander("Veja como citar o agregador")
        expander2.markdown(f"""
        <p style='text-align: center; font-family:Segoe UI;'>GERARDI, Dirceu André. <b>Agregador de pesquisas eleitorais por gênero e raça</b>: consolidação de dados de pesquisas eleitorais por raça e gênero às eleições presidenciais de 2022. Versão 1.0. São Paulo, 2022. Disponível em: XXXXX. Acesso em: 00/00/000.</p>
        """, unsafe_allow_html=True)

    with col3:
        expander5 = st.expander("Equipe")
        expander5.markdown(f"""
        <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Projeto vinclulado ao LabDados<br> e ao Núcleo de Justiça Racial e Direito da FGV Direito São Paulo</h6>
        <h6 style='text-align: center; color: #303030;font-family:Segoe UI;'>Coordenação:</h6><p style='text-align: center;'>Dirceu André Gerardi<br>(LabDados FGV)<br><br>Marta Machado<br>(FGV)<br></p></p>
        """, unsafe_allow_html=True)


