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
     page_title="Agregador de pesquisas eleitorais por gênero",
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
#         data-text="Agregador de Pesquisas eleitorais do gênero - LabDados FGV Direito SP"
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

with st.container():
    col3,col4,col5 = st.columns([.5,1.5,.5])
    with col4:
        st.markdown("""
<h5 style='text-align: center; color:#ffffff;font-family:Segoe UI,sans-serif; background-color: #578CA9;'>Projeto desenvolvido para concorrer ao<br>Prêmio Termômetro da Campanha Ipespe/Abrapel</h5>
""", unsafe_allow_html=True)

st.markdown("""
<br>
<h1 style='text-align: center; color:#202020;font-family:helvetica'>Agregador de pesquisas eleitorais por gênero</h1>
<br>
<h4 style='text-align: center; color:#54595F;font-family:Segoe UI, sans-serif'>Consolidação de pesquisas para as eleições presidenciais de 2022</h4>
""", unsafe_allow_html=True)
st.markdown("---")

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
@st.cache(allow_output_mutation=True,persist=True)
def load_dados():
    ## importa o banco
    banco =  pd.read_excel('banco_raca_genero_fgv.xlsx')
    ## lista de instituições a se considerar no banco (retirei 'prpesquisas')
    list_of_institutions = ['fsb','futura','mda','voxpopuli','quaest','ipec','poderdata','datafolha','idea','ipespe']
    ## retorna o banco filtrado
    df = banco.query('nome_instituto in @list_of_institutions')
    ## resseta o index
    df = df.reset_index(drop=True)
    return df
df = load_dados()

# @st.cache(allow_output_mutation=True)
# def load_data():
#     df = pd.read_excel('banco_raca_genero_fgv.xlsx')
#     return df
# df = load_data()

##import image logo
@st.cache(allow_output_mutation=True)
def load_image():
    agre = Image.open('fgv-logo.jpg')
    return agre
agre = load_image()


###############################################################################
## importa e plota o quadro com a lista de pesquisas utilizadas pelo agregador##
################################################################################

with st.container():
    col3,col4,col5 = st.columns([.5,4,.5])
    with col4:
        st.markdown("""
        <h4 style='text-align: center; color: #303030;font-family:Segoe UI;background-color: #F5DF4D;'><b>Informações sobre o agregador:<b></h4><br>
        """, unsafe_allow_html=True)

        ### primeiro expander, da metodologia
        expander = st.expander("Entenda como o agregador foi construído")
        expander.markdown(f"""
        <!DOCTYPE html>
        <html>
        <body>

        <p style='text-align: center; font-family:Segoe UI;'><b>Explicação:</b></p>

        <p style='text-align: justify; font-family:Segoe UI;'>🏆 O Agregador foi desenvolvido para concorrer ao Prêmio <i>Termômetro da Campanha Ipespe/Abrapel</i>;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>0. O projeto de Data Science foi construído com linguagem Python;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>1. Os institutos de pesquisa consultados são: { ', '.join(set(df['nome_instituto'].T)).title().replace('Mda','MDA').replace('Fsb','FSB').replace('Idea','Idea Big Data').replace('Voxpopuli','Vox Populi').replace('Prpesquisas','Paraná Pesquisas')};</p>
        <p style='text-align: justify; font-family:Segoe UI;'>2. O agregador de pesquisas por gênero compila dados dos levantamentos realizados pelos institutos. Não nos responsabilizamos pelas amostras ou técnicas utilizadas pelos institutos de pesquisa;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>3. Para a composição do banco de dados consideramos apenas pesquisas nacionais, tanto mais informações de Lula, Bolsonaro e Ciro Gomes no primeiro turno das eleições presidenciais e de Lula e Bolsonaro no 2º turno;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>4. A obtenção do percentual de <i>rejeição</i> dos candidatos foi por meio da resposta de eleitores que declaram "não votar de jeito nenhum” em determinado candidato;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>5. Vale destacar que os dados censitários, principais referências para a construção da amostragem das pesquisas, estão defasados. Os valores de amostragem variam conforme os critérios próprios de cada instituto de pesquisa. Os institutos utilizam dados o IBGE de 2010, da PNAD de 2021 e 2022 e também do TSE. Para termos uma noção do universo amostrado pelos institutos: Em relação a amostra de gênero dos candidatos, os <i>homens</i> variaram entre {int(df['am_h'].agg('min'))}% e {int(df['am_h'].agg('max'))}% e as <i>mulheres</i> entre {int(df['am_m'].agg('min'))}% e {int(df['am_m'].agg('max'))}%.</p> 
        <p style='text-align: justify; font-family:Segoe UI;'>6. Em relação às pesquisas, no levantamento de dados para o agregador, consideramos a última data quando os entrevistadores colheram as respostas e não a data da divulgação da pesquisa, que por interesses diversos, podem ter a sua divulgação adiada;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>7. Partindo da data da última coleta das pesquisas calculou-se a média móvel de diversas variáveis correspondendo à {m_m} dias. Mas no caso da rejeição geral utilizou-se a média móvel de {m_m15} dias;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>8. Para obter a média móvel utilizamos dados de uma série temporal e aplicamos o seguinte código Python <code>rolling().mean()</code>. Uma explicação detalhada da utilização deste código pode ser <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html">vista aqui</a>;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>9. Ao calcular a média móvel, os {m_m} primeiros resultados são omitidos dos gráficos. O objetivo principal da aplicação deste método é reduzir as oscilações no intuito de deixar as linhas dos gráficos mais fluídas. Exitem outras outras técnicas estatíticas para a redução do ruído dos dados da série temporal, tais como <i>weighted moving average, kernel smoother</i>, entre outras;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>10. O resumo das médias móveis apresentado no primeiro e segundo turnos considera e apresenta o último valor da média obtida para cada candidato;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>11. Para deixar os gráficos limpos optou-se por não inserir a margem de erro na linha da média móvel. Uma lista com as informações amostrais de cada pesquisa, incluíndo a margem de erro, poderá ser obtida na aba "pesquisas eleitorais utilizadas";</p>
        <p style='text-align: justify; font-family:Segoe UI;'>12. As imagens retrabalhadas dos candidatos que utilizamos provêm das seguintes fontes externas: <a href="https://oglobo.globo.com/epoca/o-que-dizem-os-autores-dos-programas-dos-presidenciaveis-sobre-combate-as-mudancas-climaticas-23128520">Ciro Gomes</a>, <a href="https://www.opovo.com.br/noticias/politica/2022/01/27/pesquisa-lula-tem-369-e-bolsonaro-tem-314-na-modalmais-futura.html">Lula</a>, <a href="https://www.redebrasilatual.com.br/politica/2022/02/lula-favorito-bolsonaro-tudo-nada/">Bolsonaro</a>.</p>

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
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Abrangencia das pesquisas:</h6> <p style='text-align: center';>Nacional</p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Institutos analisados:</h6> <p style='text-align: center';>{', '.join(set(df['nome_instituto'].T)).title()}</p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Método de coleta das pesquisas:</h6><p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
                Telefone: {df[df['tipo_coleta']=='telefone'].tipo_coleta.value_counts()[0]}
                <br>Presencial: {df[df['tipo_coleta']=='presencial'].tipo_coleta.value_counts()[0]}</p>
            <h6 style='text-align: center; color:#0b437e;font-family:Segoe UI;'>Contador de pesquisas para dados gerais:</h6> 
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            1º turno: {len(df[df['lul_ger_1t']>=1])}<br>
            2º turno: {len(df[df['lul_ger_2t']>=1])}</p>
            <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Contador de pesquisas com perguntas sobre gênero:</h6> 
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            1º turno: {len(df[df['lul_h_1t']>=1])}<br>
            2º turno: {len(df[df['lul_h_2t']>=1])}<br>
            </p>
        """, unsafe_allow_html=True)

        ### Como citar o agregador ####
    with col2:
        expander2 = st.expander("Veja como citar o agregador")
        expander2.markdown(f"""
        <p style='text-align: center; font-family:Segoe UI;'>GERARDI, Dirceu André. <b>Agregador de pesquisas eleitorais por gênero</b>: consolidação de dados de pesquisas eleitorais por gênero às eleições presidenciais de 2022. Versão 1.0. São Paulo, 2022. Disponível em: XXXXX. Acesso em: 00/00/000.</p>
        """, unsafe_allow_html=True)

    with col3:
        expander5 = st.expander("Equipe")
        expander5.markdown(f"""
        <h6 style='text-align: center; color: #0b437e;font-family:Segoe UI;'>Projeto desenvolvido para o<br>Prêmio: Termômetro da<br>Campanha Ipespe/Abrapel</h6>
        <h6 style='text-align: center; color: #303030;font-family:Segoe UI;'>Coordenação:</h6><p style='text-align: center;'>Dirceu André Gerardi<br>(LabDados/FGV SP)</p></p>
        """, unsafe_allow_html=True)
    

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
        Resumo - intenção de voto geral por gênero:</h3><br>
        """, unsafe_allow_html=True)

        int_vot_lula = st.checkbox('Lula')

        if int_vot_lula:

            ## coluna 1
            lul = Image.open('lulacabeça.jpg')
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
            bol = Image.open('bolso-fem.jpg')
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
            ciro = Image.open('ciro_perfil.jpg')
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
            fig.add_trace(go.Scatter(y=df[df['lul_ger_1t']>1].lul_ger_1t, x=df[df['lul_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_ger_1t']>1].lul_ger_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean(), x=df[df['lul_ger_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_1t']>1].sigla)[-1], y=list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_ger_1t']>1].bol_ger_1t, x=df[df['bol_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_ger_1t']>1].bol_ger_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean(), x=df[df['bol_ger_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_1t']>1].sigla)[-1], y=list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_1t']>1].ciro_ger_1t, x=df[df['ciro_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_ger_1t']>1].ciro_ger_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean(), x=df[df['ciro_ger_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_ger_1t']>1].sigla)[-1], y=list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 45, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Brancos e Nulos e não sabe e não respondeu

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_1t']>1].bra_nul_ns_nr_ger_1t, x=df[df['bra_nul_ns_nr_ger_1t']>1].sigla, mode='markers', name='brancos_nulos_ns_nr',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bra_nul_ns_nr_ger_1t']>1].bra_nul_ns_nr_ger_1t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_1t']>1].bra_nul_ns_nr_ger_1t.rolling(m_m).mean(), x=df[df['bra_nul_ns_nr_ger_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df[df['bra_nul_ns_nr_ger_1t']>1].sigla)[-1], y=list(df[df['bra_nul_ns_nr_ger_1t']>1].bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nul_ns_nr_ger_1t']>1].bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -20,
                        font=dict(size=20, color="black", family="Arial"))

            # ## Brancos e Nulos

            # fig.add_trace(go.Scatter(y=df.bra_nulo_ger_1t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
            #                         marker=dict(
            #                         size=5,
            #                         color=df.bra_nulo_ger_1t, #set color equal to a variable
            #                         colorscale='Greys')))

            # fig.add_trace(go.Scatter(y=df[df['bra_nulo_ger_1t']>1].bra_nulo_ger_1t.rolling(m_m).mean(), x=df[df['bra_nulo_ger_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
            #                         line=dict(color='grey', width=2.5)))

            # fig.add_annotation(x=list(df[df['bra_nulo_ger_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_ger_1t']>1].bra_nulo_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df.bra_nulo_ger_1t.rolling(m_m).mean())[-1])}%",
            #             showarrow=True,
            #             arrowhead=1,
            #             ax = 40, ay = -8,
            #             font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            <i>Média móvel das intenções de voto de candidatos à presidência - 1º turno<i><br>"""),
            title_xanchor="auto",
            plot_bgcolor='rgb(255, 255, 255)',
            paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br><br><br><br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

            ##pico segunda onda covid
            fig.add_vline(x=str("abr/21_poderdata"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            fig.add_annotation(x="abr/21_poderdata", y=57,text="Pico<br>2a onda<br>Covid-19",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            #moro desiste
            fig.add_vline(x=str("mar/22_poderdata_3"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            fig.add_annotation(x="mar/22_poderdata_3", y=57,text="Moro<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            #dória desiste
            fig.add_vline(x=str("mai/22_poderdata_2"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            fig.add_annotation(x="mai/22_poderdata_2", y=57,text="Dória<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            #candidaturas
            fig.add_annotation(x="jul/22_ipespe", y=47,text="Candidatura<br>Lula (PT)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = -30,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="jul/22_ipespe", y=30,text="Candidatura<br>Bolsonaro (PL)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 60,font=dict(size=10, color="black", family="Arial"))
            #linha inicio campanha
            fig.add_annotation(x="ago/22_fsb", y=56,text="Início da<br>Campanha<br>oficial<br>16/08",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("ago/22_fsb"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            #linha debate
            fig.add_annotation(x="ago/22_ipec_2", y=57,text="1º Debate<br>na TV",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("ago/22_ipec_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
            #linha 7 de setembro
            fig.add_annotation(x="set/22_datafolha_2", y=57,text="7 de<br>setembro",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("set/22_datafolha_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
            ##resultado 1o turno
            fig.add_annotation(x="out/22_datafolha", y=57,text="<b>Resultado<br>1º truno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha", y=52,text="Lula = 48,4%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha", y=38,text="Bolsonaro = 43,2%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha", y=13,text="Ciro = 3,0%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("out/22_datafolha"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
           
            fig.update_yaxes(range=[0,60]) ## exibe o intervalo de y a ser exibido no gráfico

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")


            # # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.15,
            #         sizex=0.14, sizey=0.14,
            #         opacity=1,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )

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
        ## Intenção de voto Geral

        # fig.add_trace(go.Scatter(y=df[df['lul_ger_1t']>1].lul_ger_1t, x=df[df['lul_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_lula',
        #                             marker=dict(
        #                             size=5,
        #                             color=df[df['lul_ger_1t']>1].lul_ger_1t, #set color equal to a variable
        #                             colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean(), x=df[df['lul_ger_1t']>1].sigla,mode='lines', name='Lula Geral',
                                line=dict(color='firebrick', width=1.5, dash='dot'),legendrank=1))

        fig.add_annotation(x=list(df[df['lul_ger_1t']>1].sigla)[-1], y=list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 15,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        # fig.add_trace(go.Scatter(y=df[df['bol_ger_1t']>1].bol_ger_1t, x=df[df['bol_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_bolsonaro',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['bol_ger_1t']>1].bol_ger_1t, #set color equal to a variable
        #                         colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean(), x=df[df['bol_ger_1t']>1].sigla,mode='lines', name='Bolsonaro Geral',
                                line=dict(color='skyblue', width=1.5, dash='dot'),legendrank=2))

        fig.add_annotation(x=list(df[df['bol_ger_1t']>1].sigla)[-1], y=list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro

        # fig.add_trace(go.Scatter(y=df[df['ciro_ger_1t']>1].ciro_ger_1t, x=df[df['ciro_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_ciro',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['ciro_ger_1t']>1].ciro_ger_1t, #set color equal to a variable
        #                         colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean(), x=df[df['ciro_ger_1t']>1].sigla, mode='lines', name='Ciro Gomes Geral',
                                line=dict(color='seagreen', width=1.5, dash='dot'),legendrank=3))

        fig.add_annotation(x=list(df[df['ciro_ger_1t']>1].sigla)[-1], y=list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 45, ay = -15,
                    font=dict(size=20, color="black", family="Arial"))

        ## Intenção de voto Feminino
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_m_1t']>1].lul_m_1t, x=df[df['lul_m_1t']>1].sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_m_1t']>1].lul_m_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean(), x=df[df['bol_m_1t']>1].sigla,mode='lines', name='Lula Mulheres',
                                line=dict(color='firebrick', width=2.5),legendrank=4))

        fig.add_annotation(x=list(df[df['lul_m_1t']>1].sigla)[-1], y=list(df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_m_1t']>1].lul_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_m_1t']>1].bol_m_1t, x=df[df['bol_m_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_m_1t']>1].bol_m_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean(), x=df[df['bol_m_1t']>1].sigla,mode='lines', name='Bolsonaro Mulheres',
                                line=dict(color='skyblue', width=2.5),legendrank=5))

        fig.add_annotation(x=list(df[df['bol_m_1t']>1].sigla)[-1], y=list(df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_m_1t']>1].bol_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro
        fig.add_trace(go.Scatter(y=df[df['ciro_m_1t']>1].ciro_m_1t, x=df[df['ciro_m_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_m_1t']>1].ciro_m_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean(), x=df[df['ciro_m_1t']>1].sigla, mode='lines', name='Ciro Gomes Mulheres',
                                line=dict(color='seagreen', width=2.5),legendrank=6))

        fig.add_annotation(x=list(df[df['ciro_m_1t']>1].sigla)[-1], y=list(df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_m_1t']>1].ciro_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos e Nulos

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t, x=df[df['bra_nulo_m_1t']>1].sigla, mode='markers', name='Brancos, nulos, NS, NR',
                                marker=dict(
                                size=5,
                                color=df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t, #set color equal to a variable
                                colorscale='Greys')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t.rolling(m_m).mean(), x=df[df['bra_nulo_m_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                line=dict(color='grey', width=2.5),legendrank=7))

        fig.add_annotation(x=list(df[df['bra_nulo_m_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_m_1t']>1].bra_nulo_m_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        # title=("""
        # Média móvel das intenções de voto de <i>mulheres</i> por candidato à presidência - 1º turno<br>
        # """),
        title_xanchor="auto",
        plot_bgcolor='rgb(255, 255, 255)',
        paper_bgcolor='rgb(255, 255, 255)',
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend_title_text='<br><br><br><br><br><br><br>',
                        legend=dict(
            orientation="v",
            font_family="arial",))

        ##pico segunda onda covid
        fig.add_vline(x=str("abr/21_poderdata"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="abr/21_poderdata", y=57,text="Pico<br>2a onda<br>Covid-19",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #moro desiste
        fig.add_vline(x=str("mar/22_poderdata_3"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="mar/22_poderdata_3", y=57,text="Moro<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #dória desiste
        fig.add_vline(x=str("mai/22_poderdata_2"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="mai/22_poderdata_2", y=57,text="Dória<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #candidaturas
        fig.add_annotation(x="jul/22_ipespe", y=47,text="Candidatura<br>Lula (PT)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = -30,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="jul/22_ipespe", y=25,text="Candidatura<br>Bolsonaro (PL)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 60,font=dict(size=10, color="black", family="Arial"))
        #linha inicio campanha
        fig.add_annotation(x="ago/22_fsb", y=56,text="Início da<br>Campanha<br>oficial<br>16/08",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_fsb"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        #linha debate
        fig.add_annotation(x="ago/22_ipec_2", y=59,text="1º Debate<br>na TV",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_ipec_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        #linha 7 de setembro
        fig.add_annotation(x="set/22_datafolha_2", y=57,text="7 de<br>setembro",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("set/22_datafolha_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        ##resultado 1o turno
        fig.add_annotation(x="out/22_datafolha", y=59,text="<b>Resultado<br>1º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha", y=54,text="Lula = 48,4%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha", y=38,text="Bolsonaro = 43,2%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha", y=15,text="Ciro = 3,0%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("out/22_datafolha"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        
        fig.update_xaxes(tickangle = 300,rangeslider_visible=False,title_font_family="Arial")

        fig.update_yaxes(range=[0,60]) ## exibe o intervalo de y a ser exibido no gráfico
        
        # # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.15,
        #         sizex=0.14, sizey=0.14,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção por gênero utilizamos {len(df[df['lul_h_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)

    if gen == 'Masculino':

        fig = go.Figure()
        ## Intenção de voto Geral

        # fig.add_trace(go.Scatter(y=df[df['lul_ger_1t']>1].lul_ger_1t, x=df[df['lul_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_lula',
        #                             marker=dict(
        #                             size=5,
        #                             color=df[df['lul_ger_1t']>1].lul_ger_1t, #set color equal to a variable
        #                             colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean(), x=df[df['lul_ger_1t']>1].sigla,mode='lines', name='Lula - geral',
                                line=dict(color='firebrick', width=1.5, dash='dot'),legendrank=1))

        fig.add_annotation(x=list(df[df['lul_ger_1t']>1].sigla)[-1], y=list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        # fig.add_trace(go.Scatter(y=df[df['bol_ger_1t']>1].bol_ger_1t, x=df[df['bol_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_bolsonaro',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['bol_ger_1t']>1].bol_ger_1t, #set color equal to a variable
        #                         colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean(), x=df[df['bol_ger_1t']>1].sigla,mode='lines', name='Bolsonaro - geral',
                                line=dict(color='skyblue', width=1.5, dash='dot'),legendrank=2))

        fig.add_annotation(x=list(df[df['bol_ger_1t']>1].sigla)[-1], y=list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro

        # fig.add_trace(go.Scatter(y=df[df['ciro_ger_1t']>1].ciro_ger_1t, x=df[df['ciro_ger_1t']>1].sigla, mode='markers', name='int_vot_geral_ciro',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['ciro_ger_1t']>1].ciro_ger_1t, #set color equal to a variable
        #                         colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean(), x=df[df['ciro_ger_1t']>1].sigla, mode='lines', name='Ciro Gomes - geral',
                                line=dict(color='seagreen', width=1.5, dash='dot'),legendrank=3))

        fig.add_annotation(x=list(df[df['ciro_ger_1t']>1].sigla)[-1], y=list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 45, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))


        ###### Intenção de voto Masculino
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_h_1t']>1].lul_h_1t, x=df[df['lul_h_1t']>1].sigla, mode='markers', name='Int. voto. Lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_h_1t']>1].lul_h_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean(), x=df[df['bol_h_1t']>1].sigla,mode='lines', name='Lula - Homens',
                                line=dict(color='firebrick', width=2.5),legendrank=4))

        fig.add_annotation(x=list(df[df['lul_h_1t']>1].sigla)[-1], y=list(df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_h_1t']>1].lul_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -1.20,
                    font=dict(size=20, color="black", family="Arial"))
        
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_h_1t']>1].bol_h_1t, x=df[df['bol_h_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_h_1t']>1].bol_h_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean(), x=df[df['bol_h_1t']>1].sigla,mode='lines', name='Bolsonaro - Homens',
                                line=dict(color='skyblue', width=2.5),legendrank=5))

        fig.add_annotation(x=list(df[df['bol_h_1t']>1].sigla)[-1], y=list(df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_h_1t']>1].bol_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Ciro
        fig.add_trace(go.Scatter(y=df[df['ciro_h_1t']>1].ciro_h_1t, x=df[df['ciro_h_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_h_1t']>1].ciro_h_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean(), x=df[df['ciro_h_1t']>1].sigla, mode='lines', name='Ciro Gomes - Homens',
                                line=dict(color='seagreen', width=2.5),legendrank=6))

        fig.add_annotation(x=list(df[df['ciro_h_1t']>1].sigla)[-1], y=list(df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_h_1t']>1].ciro_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos e Nulos

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t, x=df[df['bra_nulo_h_1t']>1].sigla, mode='markers', name='Brancos, nulos, NS, NR',
                                marker=dict(
                                size=5,
                                color=df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t, #set color equal to a variable
                                colorscale='Greys')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t.rolling(m_m).mean(), x=df[df['bra_nulo_h_1t']>1].sigla, mode='lines', name='Brancos, nulos, NS, NR',
                                line=dict(color='grey', width=2.5),legendrank=7))

        fig.add_annotation(x=list(df[df['bra_nulo_h_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_h_1t']>1].bra_nulo_h_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>homens</i> por candidato à presidência - 1º turno<br>
        """),
        title_xanchor="auto",
        plot_bgcolor='rgb(255, 255, 255)',
        paper_bgcolor='rgb(255, 255, 255)',
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        font=dict(family="arial",size=13),
                        legend_title_text='<br><br><br><br><br><br><br>',
                        legend=dict(
            orientation="v",
            font_family="arial",))

        ##pico segunda onda covid
        fig.add_vline(x=str("abr/21_poderdata"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="abr/21_poderdata", y=57,text="Pico<br>2a onda<br>Covid-19",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #moro desiste
        fig.add_vline(x=str("mar/22_poderdata_3"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="mar/22_poderdata_3", y=57,text="Moro<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #dória desiste
        fig.add_vline(x=str("mai/22_poderdata_2"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="mai/22_poderdata_2", y=57,text="Dória<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #candidaturas
        fig.add_annotation(x="jul/22_ipespe", y=45,text="Candidatura<br>Lula (PT)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = -30,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="jul/22_ipespe", y=32,text="Candidatura<br>Bolsonaro (PL)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 60,font=dict(size=10, color="black", family="Arial"))
        #linha inicio campanha
        fig.add_annotation(x="ago/22_fsb", y=57,text="Início da<br>Campanha<br>oficial<br>16/08",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_fsb"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        #linha debate
        fig.add_annotation(x="ago/22_ipec_2", y=57,text="1º Debate<br>na TV",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_ipec_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        #linha 7 de setembro
        fig.add_annotation(x="set/22_datafolha_2", y=57,text="7 de<br>setembro",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("set/22_datafolha_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        ##resultado 1o turno
        fig.add_annotation(x="out/22_datafolha", y=57,text="<b>Resultado<br>1º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha", y=52,text="Lula = 48,4%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha", y=28,text="Bolsonaro = 43,2%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha", y=13,text="Ciro = 3,0%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("out/22_datafolha"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)

        fig.update_xaxes(tickangle = 300,rangeslider_visible=False,title_font_family="Arial")

        fig.update_yaxes(range=[0,60]) ## exibe o intervalo de y a ser exibido no gráfico

        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.15,
        #         sizex=0.14, sizey=0.14,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto por gênero utilizamos {len(df[df['lul_h_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")

    ###################################
    ## Intenção de voto por raça ##
    ###################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por raça:</h3><br>
        """, unsafe_allow_html=True)
        raça = st.selectbox('Selecione a raça:',options=['--Escolha a opção--','Parda', 'Branca', 'Preta', 'Outras'])

    if raça == 'Parda':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_par_1t']>1].lul_par_1t, x=df[df['lul_par_1t']>1].sigla, mode='markers', name='int_vot_par_lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_par_1t']>1].lul_par_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_par_1t']>1].lul_par_1t .rolling(m_m).mean(), x=df[df['bol_par_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_par_1t']>1].sigla)[-1], y=list(df[df['lul_par_1t']>1].lul_par_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_par_1t']>1].lul_par_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_par_1t']>1].bol_par_1t, x=df[df['bol_par_1t']>1].sigla, mode='markers', name='int_vot_par_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_par_1t']>1].lul_par_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean(), x=df[df['bol_par_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_par_1t']>1].sigla)[-1], y=list(df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_par_1t']>1].bol_par_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro

        fig.add_trace(go.Scatter(y=df[df['ciro_par_1t']>1].ciro_par_1t, x=df[df['ciro_par_1t']>1].sigla, mode='markers', name='int_vot_par_ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_par_1t']>1].ciro_par_1t, #set color equal to a variable
                                colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean(), x=df[df['ciro_par_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_par_1t']>1].sigla)[-1], y=list(df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_par_1t']>1].ciro_par_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>pardos</i> por candidato à presidência - 1º turno<br>
        """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Intenção de voto (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

        fig.add_annotation(x="mar/22_poderdata_3", y=25,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.20,
        #         sizex=0.12, sizey=0.12,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig)

    if raça == 'Branca':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_bra_1t']>1].lul_bra_1t, x=df[df['lul_bra_1t']>1].sigla, mode='markers', name='int_vot_bra_lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_bra_1t']>1].lul_bra_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean(), x=df[df['bol_bra_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_bra_1t']>1].sigla)[-1], y=list(df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_bra_1t']>1].lul_bra_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_bra_1t']>1].bol_bra_1t, x=df[df['bol_bra_1t']>1].sigla, mode='markers', name='int_vot_bra_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_bra_1t']>1].lul_bra_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean(), x=df[df['bol_bra_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_bra_1t']>1].sigla)[-1], y=list(df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_bra_1t']>1].bol_bra_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Ciro
        fig.add_trace(go.Scatter(y=df[df['ciro_bra_1t']>1].ciro_bra_1t, x=df[df['ciro_bra_1t']>1].sigla, mode='markers', name='int_vot_bra_ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_bra_1t']>1].ciro_bra_1t, #set color equal to a variable
                                colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean(), x=df[df['ciro_bra_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_bra_1t']>1].sigla)[-1], y=list(df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_bra_1t']>1].ciro_bra_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>brancos</i> por candidato à presidência - 1º turno<br>
        """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Intenção de voto (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

        fig.add_annotation(x="mar/22_poderdata_3", y=28,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False, title_font_family="Arial")
        
        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.20,
        #         sizex=0.12, sizey=0.12,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig)

    if raça == 'Preta':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_pre_1t']>1].lul_pre_1t, x=df[df['lul_pre_1t']>1].sigla, mode='markers', name='int_vot_lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_pre_1t']>1].lul_pre_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean(), x=df[df['bol_pre_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_pre_1t']>1].sigla)[-1], y=list(df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_pre_1t']>1].lul_pre_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_pre_1t']>1].bol_pre_1t, x=df[df['bol_pre_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_pre_1t']>1].lul_pre_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean(), x=df[df['bol_pre_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_pre_1t']>1].sigla)[-1], y=list(df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_pre_1t']>1].bol_pre_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro
        fig.add_trace(go.Scatter(y=df[df['ciro_pre_1t']>1].ciro_pre_1t, x=df[df['ciro_pre_1t']>1].sigla, mode='markers', name='int_vot_ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_pre_1t']>1].ciro_pre_1t, #set color equal to a variable
                                colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean(), x=df[df['ciro_pre_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_pre_1t']>1].sigla)[-1], y=list(df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_pre_1t']>1].ciro_pre_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>pretos</i> por candidato à presidência - 1º turno<br>
        """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Intenção de voto (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

        fig.add_annotation(x="mar/22_poderdata_3", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

      
        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.19,
        #         sizex=0.14, sizey=0.14,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig)

    if raça == 'Outras':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_out_1t']>1].lul_out_1t, x=df[df['lul_out_1t']>1].sigla, mode='markers', name='int_vot_lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_out_1t']>1].lul_out_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean(), x=df[df['bol_out_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_out_1t']>1].sigla)[-1], y=list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_out_1t']>1].bol_out_1t, x=df[df['bol_out_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_out_1t']>1].lul_out_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean(), x=df[df['bol_out_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_out_1t']>1].sigla)[-1], y=list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro

        fig.add_trace(go.Scatter(y=df[df['ciro_out_1t']>1].ciro_out_1t, x=df[df['ciro_out_1t']>1].sigla, mode='markers', name='int_vot_ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_out_1t']>1].ciro_out_1t, #set color equal to a variable
                                colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean(), x=df[df['ciro_out_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_out_1t']>1].sigla)[-1], y=list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>outras</i> candidato à presidência - 1º turno<br>
        """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Intenção de voto (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

        fig.add_annotation(x="mar/22_futura", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_futura", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.20,
        #         sizex=0.12, sizey=0.12,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig)

        ## info
    st.markdown(f"""
    <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
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
            ##drop 'Parda', 'Branca', 'Preta', 'Outras', 
            raça2 = st.selectbox('Escolha o gênero:',options=['--Selecione uma opção--','Mulheres', 'Homens'])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            if raça2 == 'Homens':

                fonte = df.query(f"nome_instituto =='{inst}'")
                genero_escolhido = 'h'
                genero = 'homens'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'lul_{genero_escolhido}_1t']>1][f'lul_{genero_escolhido}_1t'], mode='lines+markers', name=f"Lula - {genero}",
                                        line=dict(color='firebrick', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['lul_ger_1t']>1].lul_ger_1t, mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=1))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'bol_{genero_escolhido}_1t']>1][f'bol_{genero_escolhido}_1t'], mode='lines+markers', name=f"Bolsonaro - {genero}",
                                        line=dict(color='royalblue', width=2.5),legendrank=4))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['bol_ger_1t']>1].bol_ger_1t, mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=3))
                
                fig.update_layout(width = 900, height = 700, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{genero}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                        plot_bgcolor='rgb(255, 255, 255)',
                        paper_bgcolor='rgb(255, 255, 255)',
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend_title_text='<br><br><br><br>Legenda:<br>',
                                        legend=dict(
                                                orientation="v",
                                                font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])


                # Add image
                # fig.add_layout_image(
                #     dict(
                #         source=agre,
                #         xref="paper", yref="paper",
                #         x=.99, y=1.08,
                #         sizex=0.14, sizey=0.14,
                #         xanchor="right", yanchor="bottom"
                #     )
                # )
                
                st.plotly_chart(fig)


            if raça2 == 'Mulheres':

                fonte = df.query(f"nome_instituto =='{inst}'")
                genero_escolhido = 'm'
                genero = 'mulheres'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'lul_{genero_escolhido}_1t']>1][f'lul_{genero_escolhido}_1t'], mode='lines+markers', name=f"Lula - {genero}",
                                        line=dict(color='firebrick', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['lul_ger_1t']>1].lul_ger_1t,mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=1))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'bol_{genero_escolhido}_1t']>1][f'bol_{genero_escolhido}_1t'], mode='lines+markers', name=f"Bolsonaro - {genero}",
                                        line=dict(color='royalblue', width=2.5),legendrank=4))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['bol_ger_1t']>1].bol_ger_1t,mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=3))
                
                fig.update_layout(width = 900, height = 700, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=15, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{genero}' por candidato - {inst.title()} (1º turno)
                        <br>
                        <br>
                        """),
                        plot_bgcolor='rgb(255, 255, 255)',
                        paper_bgcolor='rgb(255, 255, 255)',
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        legend_title_text='<br><br><br><br>Legenda:<br>',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                                                orientation="v",
                                                font_family="arial",))

                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])


                # # Add image
                # fig.add_layout_image(
                #     dict(
                #         source=agre,
                #         xref="paper", yref="paper",
                #         x=.99, y=1.08,
                #         sizex=0.14, sizey=0.14,
                #         xanchor="right", yanchor="bottom"
                #     )
                # )
                
                st.plotly_chart(fig)
               
        
        st.markdown(f"""
        <h7 style='text-align: center; color: black; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte de gênero. No entanto, nem todos os institutos coletam tais informações. Assim, se a combinação selecionada retornar apenas os dados de intenção de voto geral, isso significa, que o instituto selecionado não coletou a informação.</h7>
        """, unsafe_allow_html=True)


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
        Resumo - Rejeição geral e por gênero segundo candidato:</h3><br>
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
            fig.add_trace(go.Scatter(y=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t, x=df[df['lul_ger_rej_1t']>1].sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean(), x=df[df['lul_ger_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_rej_1t']>1].sigla)[-1], y=list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean())[-1],text=f"{int(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -0.05,
                        font=dict(size=20, color="black", family="Arial"))

            ## bolsonaro

            fig.add_trace(go.Scatter(y=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t, x=df[df['bol_ger_rej_1t']>1].sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean(), x=df[df['bol_ger_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_rej_1t']>1].sigla)[-1], y=list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean())[-1],text=f"{int(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t, x=df[df['ciro_ger_rej_1t']>1].sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean(), x=df[df['ciro_ger_rej_1t']>1].sigla,mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_ger_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean())[-1],text=f"{int(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            <i>Rejeição geral dos candidatos à presidência (1º turno)<i><br><br>
            """),
            title_xanchor="auto",
            plot_bgcolor='rgb(255, 255, 255)',
            paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br><br><br><br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

            
            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            fig.update_yaxes(range=[0,70])

            # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.15,
            #         sizex=0.14, sizey=0.14,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )
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
        fig.add_trace(go.Scatter(y=df[df['lul_m_rej_1t']>1].lul_m_rej_1t, x=df[df['lul_m_rej_1t']>1].sigla, mode='markers', name='int_voto_lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_m_rej_1t']>1].lul_m_rej_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean(), x=df[df['bol_m_rej_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_m_rej_1t']>1].sigla)[-1], y=list(df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_m_rej_1t']>1].lul_m_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_m_rej_1t']>1].bol_m_rej_1t, x=df[df['bol_m_rej_1t']>1].sigla, mode='markers', name='int_voto_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_m_rej_1t']>1].lul_m_rej_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean(), x=df[df['bol_m_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_m_rej_1t']>1].sigla)[-1], y=list(df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_m_rej_1t']>1].bol_m_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro
        fig.add_trace(go.Scatter(y=df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t, x=df[df['ciro_m_rej_1t']>1].sigla, mode='markers', name='int_voto_ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean(), x=df[df['ciro_m_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_m_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_m_rej_1t']>1].ciro_m_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel da rejeição de <i>mulheres</i> por candidato à presidência - 1º turno<br>
        """),
        title_xanchor="auto",
        plot_bgcolor='rgb(255, 255, 255)',
        paper_bgcolor='rgb(255, 255, 255)',
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Rejeição (%)',
                        font=dict(family="arial",size=13),
                        legend_title_text='<br><br><br><br><br><br><br>',
                        legend=dict(
            orientation="v",
            font_family="arial",))

        
        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        
        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.20,
        #         sizex=0.14, sizey=0.14,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

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
        fig.add_trace(go.Scatter(y=df[df['lul_h_rej_1t']>1].lul_h_rej_1t, x=df[df['lul_h_rej_1t']>1].sigla, mode='markers', name='int_vot_lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_h_rej_1t']>1].lul_h_rej_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean(), x=df[df['bol_h_rej_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_h_rej_1t']>1].sigla)[-1], y=list(df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_h_rej_1t']>1].lul_h_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_h_rej_1t']>1].bol_h_rej_1t, x=df[df['bol_h_rej_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_h_rej_1t']>1].bol_h_rej_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean(), x=df[df['bol_h_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_h_rej_1t']>1].sigla)[-1], y=list(df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_h_rej_1t']>1].bol_h_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Ciro
        fig.add_trace(go.Scatter(y=df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t, x=df[df['ciro_h_rej_1t']>1].sigla, mode='markers', name='int_vot_ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t, #set color equal to a variable
                                colorscale='Aggrnyl')))

        fig.add_trace(go.Scatter(y=df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean(), x=df[df['ciro_h_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_h_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_h_rej_1t']>1].ciro_h_rej_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel da rejeição de <i>homens</i> por candidato à presidência - 1º turno<br>
        """),
        title_xanchor="auto",
        plot_bgcolor='rgb(255, 255, 255)',
        paper_bgcolor='rgb(255, 255, 255)',
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Rejeição (%)',
                        font=dict(family="arial",size=13),
                        legend_title_text='<br><br><br><br><br><br><br>',
                        legend=dict(
            orientation="v",
            font_family="arial",))


        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.20,
        #         sizex=0.12, sizey=0.12,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

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

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Helvetica; text-rendering: optimizelegibility; background-color: #EAE6DA;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição por Raça:</h3><br>
        """, unsafe_allow_html=True)
        
        raça3 = st.selectbox('Selecione a raça:',options=[' --Escolha a opção--',' Parda', ' Branca', ' Preta', ' Outras'])

        if raça3 == ' Parda':

            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_par_rej_1t']>1].lul_par_rej_1t, x=df[df['lul_par_rej_1t']>1].sigla, mode='markers', name='int_vot_par_lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_par_rej_1t']>1].lul_par_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_par_rej_1t']>1].lul_par_rej_1t .rolling(m_m).mean(), x=df[df['lul_par_rej_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_par_rej_1t']>1].sigla)[-1], y=list(df[df['lul_par_rej_1t']>1].lul_par_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_par_rej_1t']>1].lul_par_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_par_rej_1t']>1].bol_par_rej_1t, x=df[df['bol_par_rej_1t']>1].sigla, mode='markers', name='int_vot_par_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_par_rej_1t']>1].lul_par_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean(), x=df[df['bol_par_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_par_rej_1t']>1].sigla)[-1], y=list(df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_par_rej_1t']>1].bol_par_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t, x=df[df['ciro_par_rej_1t']>1].sigla, mode='markers', name='int_vot_par_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean(), x=df[df['ciro_par_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_par_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_par_rej_1t']>1].ciro_par_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            Média móvel da rejeição de <i>pardos</i> por candidato à presidência - 1º turno<br>
            """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Rejeição (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

            fig.add_annotation(x="mar/22_poderdata_3", y=25,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.20,
            #         sizex=0.12, sizey=0.12,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )

            st.plotly_chart(fig)

        if raça3 == ' Branca':
            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t, x=df[df['lul_bra_rej_1t']>1].sigla, mode='markers', name='int_vot_bra_lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean(), x=df[df['lul_bra_rej_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_bra_rej_1t']>1].sigla)[-1], y=list(df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_bra_rej_1t']>1].lul_bra_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))
            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t, x=df[df['bol_bra_rej_1t']>1].sigla, mode='markers', name='int_vot_bra_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_bra_rej_1t']>1].lul_bra_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean(), x=df[df['bol_bra_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_bra_rej_1t']>1].sigla)[-1], y=list(df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_bra_rej_1t']>1].bol_bra_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))
            ## Ciro
            fig.add_trace(go.Scatter(y=df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t, x=df[df['ciro_bra_rej_1t']>1].sigla, mode='markers', name='int_vot_bra_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean(), x=df[df['ciro_bra_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_bra_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_bra_rej_1t']>1].ciro_bra_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            Média móvel da rejeição de <i>brancos</i> por candidato à presidência - 1º turno<br>
            """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Rejeição (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

            fig.add_annotation(x="mar/22_poderdata_3", y=28,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")
            
            # # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.20,
            #         sizex=0.12, sizey=0.12,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )

            st.plotly_chart(fig)

        if raça3 == ' Preta':
            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t, x=df[df['lul_pre_rej_1t']>1].sigla, mode='markers', name='int_vot_lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean(), x=df[df['lul_pre_rej_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_pre_rej_1t']>1].sigla)[-1], y=list(df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_pre_rej_1t']>1].lul_pre_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t, x=df[df['bol_pre_rej_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean(), x=df[df['bol_pre_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_pre_rej_1t']>1].sigla)[-1], y=list(df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_pre_rej_1t']>1].bol_pre_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro
            fig.add_trace(go.Scatter(y=df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t, x=df[df['ciro_pre_rej_1t']>1].sigla, mode='markers', name='int_vot_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean(), x=df[df['ciro_pre_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_pre_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_pre_rej_1t']>1].ciro_pre_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            Média móvel da rejeição de <i>pretos</i> por candidato à presidência - 1º turno<br>
            """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Rejeição (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

            fig.add_annotation(x="mar/22_poderdata_3", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        
            # # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.19,
            #         sizex=0.14, sizey=0.14,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )

            st.plotly_chart(fig)

        if raça3 == ' Outras':
            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_out_rej_1t']>1].lul_out_rej_1t, x=df[df['lul_out_rej_1t']>1].sigla, mode='markers', name='int_vot_lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_out_rej_1t']>1].lul_out_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean(), x=df[df['lul_out_rej_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_out_rej_1t']>1].sigla)[-1], y=list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_out_rej_1t']>1].bol_out_rej_1t, x=df[df['bol_out_rej_1t']>1].sigla, mode='markers', name='int_vot_bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_out_rej_1t']>1].bol_out_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean(), x=df[df['bol_out_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_out_rej_1t']>1].sigla)[-1], y=list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t, x=df[df['ciro_out_rej_1t']>1].sigla, mode='markers', name='int_vot_ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean(), x=df[df['ciro_out_rej_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_out_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            Média móvel da rejeição de <i>outras</i> candidato à presidência - 1º turno<br>
            """),
                title_xanchor="auto",
                plot_bgcolor='rgb(255, 255, 255)',
                paper_bgcolor='rgb(255, 255, 255)',
                                xaxis_title='Mês, ano e instituto de pesquisa',
                                yaxis_title='Rejeição (%)',
                                font=dict(family="arial",size=13),
                                legend_title_text='<br><br><br><br><br><br><br>',
                                legend=dict(
                    orientation="v",
                    font_family="arial"))

            fig.add_annotation(x="mar/22_futura", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_futura", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=True,title_font_family="Arial")

            # # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.20,
            #         sizex=0.12, sizey=0.12,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )

            st.plotly_chart(fig)


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

            if raça4 == ' Homens ':

                fonte = df.query(f"nome_instituto =='{inst}'")
                genero_escolhido = 'h'
                genero = 'homens'

                fig = go.Figure()

                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'lul_{genero_escolhido}_rej_1t']>1][f'lul_{genero_escolhido}_rej_1t'], mode='lines+markers', name=f"Lula - {genero}",
                                        line=dict(color='firebrick', width=2.5),legendrank=2))                
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['lul_ger_rej_1t']>1].lul_ger_rej_1t, mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=1))
                
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'bol_{genero_escolhido}_rej_1t']>1][f'bol_{genero_escolhido}_rej_1t'], mode='lines+markers', name=f"Bolsonaro - {genero}",
                                        line=dict(color='royalblue', width=2.5),legendrank=4))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['bol_ger_rej_1t']>1].bol_ger_rej_1t, mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=3))
        
                
                fig.update_layout(width = 900, height = 700, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=15, t=150),
                        title=(f"""
                        Rejeição 'geral' e de '{genero}' por candidato - {inst.title()} (1º turno)
                        <br>
                        <br>
                        """),
                            title_xanchor="auto",
                            plot_bgcolor='rgb(255, 255, 255)',
                            paper_bgcolor='rgb(255, 255, 255)',
                                            xaxis_title='Mês, ano e instituto de pesquisa',
                                                        yaxis_title='Rejeição (%)',
                                                        font=dict(family="arial",size=13),
                                                        legend_title_text='<br><br><br><br>Legenda:<br>',
                                                        legend=dict(
                                                        orientation="v",
                                                        font_family="arial",))

                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])


                # # Add image
                # fig.add_layout_image(
                #     dict(
                #         source=agre,
                #         xref="paper", yref="paper",
                #         x=.99, y=1.08,
                #         sizex=0.14, sizey=0.14,
                #         xanchor="right", yanchor="bottom"
                #     )
                # )
                
                st.plotly_chart(fig)


            if raça4 == ' Mulheres ':

                fonte = df.query(f"nome_instituto =='{inst}'")
                genero_escolhido = 'm'
                genero = 'mulheres'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'lul_{genero_escolhido}_rej_1t']>1][f'lul_{genero_escolhido}_rej_1t'], mode='lines+markers', name=f"Lula - {genero}",
                                        line=dict(color='firebrick', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['lul_ger_rej_1t']>1].lul_ger_rej_1t,mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=1))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte[f'bol_{genero_escolhido}_rej_1t']>1][f'bol_{genero_escolhido}_rej_1t'], mode='lines+markers', name=f"Bolsonaro - {genero}",
                                        line=dict(color='royalblue', width=2.5),legendrank=4))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[fonte['bol_ger_rej_1t']>1].bol_ger_rej_1t,mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=3))
                
                fig.update_layout(width = 800, height = 700, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=15, t=150),
                        #title=(f"""
                        # Rejeição 'geral' e de '{genero}' por candidato - {inst.title()} (1º turno)
                        # <br>
                        # <br>
                        # """),
                        plot_bgcolor='rgb(255, 255, 255)',
                        paper_bgcolor='rgb(255, 255, 255)',
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Rejeição (%)',
                                        font=dict(family="arial",size=13),
                                        legend_title_text='<br><br><br><br>Legenda:<br>',
                                        legend=dict(
                                                orientation="v",
                                                font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])


                # # Add image
                # fig.add_layout_image(
                #     dict(
                #         source=agre,
                #         xref="paper", yref="paper",
                #         x=.99, y=1.08,
                #         sizex=0.14, sizey=0.14,
                #         xanchor="right", yanchor="bottom"
                #     )
                # )
                
                st.plotly_chart(fig)
               
        
        st.markdown(f"""
        <h7 style='text-align: center; color: black; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte de gênero. No entanto, nem todos os institutos coletam tais informações. Assim, se a combinação selecionada retornar apenas os dados da rejeição geral, isso significa, que o instituto selecionado não coletou a informação.</h7>
        """, unsafe_allow_html=True)


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
            lul = Image.open('lulacabeça.jpg')
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
            bol = Image.open('bolso-fem.jpg')
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
            fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t, x=df[df['lul_ger_2t']>1].sigla, mode='markers', name='Int. voto Lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_ger_2t']>1].lul_ger_2t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean(), x=df[df['lul_ger_2t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_2t']>1].sigla)[-1], y=list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                    ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t, x=df[df['bol_ger_2t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_ger_2t']>1].bol_ger_2t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_2t']>1].sigla)[-1], y=list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                    ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            # ## Brancos e Nulos e não sabe e não respondeu

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t, x=df[df['bra_nul_ns_nr_ger_2t']>1].sigla, mode='markers', name='Brancos, nulos, NS, NR',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean(), x=df[df['bra_nul_ns_nr_ger_2t']>1].sigla, mode='lines', name='Brancos, nulos, NS, NR',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df[df['bra_nul_ns_nr_ger_2t']>1].sigla)[-1], y=list(df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean())[-1])}%",
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

            # fig.add_annotation(x=list(df[df['bra_nulo_ger_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_ger_2t']>1].bra_nulo_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_ger_2t']>1].bra_nulo_ger_2t.rolling(m_m).mean())[-1])}%",
            #             showarrow=True,
            #             arrowhead=1,
            #             ax = 40, ay = -8,
            #             font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
            title=("""
            Média móvel das intenções de voto geral por candidato à presidência (2º turno)<br>
            """),
            title_xanchor="auto",
            plot_bgcolor='rgb(255, 255, 255)',
            paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br><br><br><br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

            ##pico segunda onda covid
            fig.add_vline(x=str("abr/21_poderdata"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            fig.add_annotation(x="abr/21_poderdata", y=63,text="Pico<br>2a onda<br>Covid-19",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            #moro desiste
            fig.add_vline(x=str("mar/22_poderdata_3"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            fig.add_annotation(x="mar/22_poderdata_3", y=63,text="Moro<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            #dória desiste
            fig.add_vline(x=str("mai/22_poderdata_2"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            fig.add_annotation(x="mai/22_poderdata_2", y=63,text="Dória<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            #candidaturas
            fig.add_annotation(x="jul/22_ipespe", y=53,text="Candidatura<br>Lula (PT)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = -30,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="jul/22_ipespe", y=35,text="Candidatura<br>Bolsonaro (PL)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 60,font=dict(size=10, color="black", family="Arial"))
            #linha inicio campanha
            fig.add_annotation(x="ago/22_fsb", y=61,text="Início da<br>Campanha<br>oficial<br>16/08",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("ago/22_fsb"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            #linha debate
            fig.add_annotation(x="ago/22_ipec_2", y=64,text="1º Debate<br>na TV",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("ago/22_ipec_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
            #linha 7 de setembro
            fig.add_annotation(x="set/22_datafolha_2", y=63,text="7 de<br>setembro",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("set/22_datafolha_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
            ##resultado 1o turno
            fig.add_annotation(x="out/22_datafolha", y=63,text="<b>Resultado<br>1º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha", y=58,text="Lula = 48,4%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha", y=31,text="Bolsonaro = 43,2%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("out/22_datafolha"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
            ##resultado 2o turno
            fig.add_annotation(x="out/22_datafolha_6", y=63,text="<b>Resultado<br>2º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha_6", y=58,text="Lula = 50,9%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="out/22_datafolha_6", y=31,text="Bolsonaro = 49,1%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_vline(x=str("out/22_datafolha_6"), line_width=.5, line_dash="dot", line_color="black", opacity=.4)

            fig.update_xaxes(tickangle = 300,rangeslider_visible=False,title_font_family="Arial")
            fig.update_yaxes(range=[0,65])

            # Add image
            # fig.add_layout_image(
            #     dict(
            #         source=agre,
            #         xref="paper", yref="paper",
            #         x=.99, y=1.20,
            #         sizex=0.14, sizey=0.14,
            #         xanchor="right", yanchor="bottom"
            #     )
            # )

            st.plotly_chart(fig,use_container_width=True)
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
        ## intenção de voto geral

        ## lula
        # fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t, x=df[df['lul_ger_2t']>1].sigla, mode='markers', name='Int. voto geral Lula',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['lul_ger_2t']>1].lul_ger_2t, #set color equal to a variable
        #                         colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean(), x=df[df['lul_ger_2t']>1].sigla,mode='lines', name='Lula Geral',
                                line=dict(color='firebrick', width=1.5, dash='dot')))

        fig.add_annotation(x=list(df[df['lul_ger_2t']>1].sigla)[-1], y=list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        # fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t, x=df[df['bol_ger_2t']>1].sigla, mode='markers', name='Int. voto geral Bolsonaro',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['bol_ger_2t']>1].bol_ger_2t, #set color equal to a variable
        #                         colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Bolsonaro Geral',
                                line=dict(color='skyblue', width=1.5, dash='dot')))

        fig.add_annotation(x=list(df[df['bol_ger_2t']>1].sigla)[-1], y=list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))



        ### intenção de voto Mulheres
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_m_2t, x=df.sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df.lul_m_2t, #set color equal to a variable
                                colorscale='peach'),legendrank=2))

        fig.add_trace(go.Scatter(y=df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean(), x=df[df['lul_m_2t']>1].sigla,mode='lines', name='Lula mulheres',
                                line=dict(color='firebrick', width=2.5),legendrank=1))

        fig.add_annotation(x=list(df[df['lul_m_2t']>1].sigla)[-1], y=list(df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_m_2t']>1].lul_m_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_m_2t, x=df.sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_m_2t, #set color equal to a variable
                                colorscale='ice'),legendrank=4))

        fig.add_trace(go.Scatter(y=df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean(), x=df[df['bol_m_2t']>1].sigla,mode='lines', name='Bolsonaro Mulheres',
                                line=dict(color='skyblue', width=2.5),legendrank=3))

        fig.add_annotation(x=list(df[df['bol_m_2t']>1].sigla)[-1], y=list(df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_m_2t']>1].bol_m_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                       ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos, Nulos 
        fig.add_trace(go.Scatter(y=df.bra_nulo_m_2t, x=df.sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df[df['bra_nulo_m_2t']>1].bra_nulo_m_2t, #set color equal to a variable
                                colorscale='gray'),legendrank=6))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_m_2t']>1].bra_nulo_m_2t.rolling(m_m).mean(), x=df[df['bra_nulo_m_2t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='gray', width=2.5),legendrank=5))

        fig.add_annotation(x=list(df[df['bra_nulo_m_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_m_2t']>1].bra_nulo_m_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nulo_m_2t']>1].bra_nulo_m_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1150, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>mulheres</i> por candidato à presidência (2º turno)<br>
        """),
            title_xanchor="auto",
            plot_bgcolor='rgb(255, 255, 255)',
            paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br><br><br><br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

        ##pico segunda onda covid
        fig.add_vline(x=str("abr/21_poderdata"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="abr/21_poderdata", y=65,text="Pico<br>2a onda<br>Covid-19",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #moro desiste
        fig.add_vline(x=str("mar/22_poderdata_3"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="mar/22_poderdata_3", y=65,text="Moro<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #dória desiste
        # fig.add_vline(x=str("mai/22_poderdata_2"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        # fig.add_annotation(x="mai/22_poderdata_2", y=63,text="Dória<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        # #candidaturas
        fig.add_annotation(x="jul/22_ipespe", y=56,text="Candidatura<br>Lula (PT)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = -30,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="jul/22_ipespe", y=31,text="Candidatura<br>Bolsonaro (PL)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 60,font=dict(size=10, color="black", family="Arial"))
        #linha inicio campanha
        fig.add_annotation(x="ago/22_fsb", y=65,text="Início da<br>Campanha<br>oficial<br>16/08",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_fsb"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        #linha debate
        fig.add_annotation(x="ago/22_ipec_2", y=65,text="1º Debate<br>na TV",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_ipec_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        #linha 7 de setembro
        fig.add_annotation(x="set/22_datafolha_2", y=64,text="7 de<br>setembro",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("set/22_datafolha_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        ##resultado 1o turno
        fig.add_annotation(x="out/22_ipec", y=65,text="<b>Resultado<br>1º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_ipec", y=58,text="Lula = 48,4%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_ipec", y=31,text="Bolsonaro = 43,2%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("out/22_ipec"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)        
        # ##resultado 2o turno
        fig.add_annotation(x="out/22_datafolha_6", y=65,text="<b>Resultado<br>2º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha_6", y=58,text="Lula = 50,9%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha_6", y=31,text="Bolsonaro = 49,1%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("out/22_datafolha_6"), line_width=.5, line_dash="dot", line_color="black", opacity=.4)

        fig.update_xaxes(tickangle = 300,rangeslider_visible=False,title_font_family="Arial")
        fig.update_yaxes(range=[0,65])

        
        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.15,
        #         sizex=0.14, sizey=0.14,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig,use_container_width=True)

        ## info
        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto por gênero utilizamos {len(df[df['lul_h_2t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)

    if gen5 == ' Masculino':

        fig = go.Figure()

        ## intenção de voto geral

        ## lula
        # fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t, x=df[df['lul_ger_2t']>1].sigla, mode='markers', name='Int. voto geral Lula',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['lul_ger_2t']>1].lul_ger_2t, #set color equal to a variable
        #                         colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean(), x=df[df['lul_ger_2t']>1].sigla,mode='lines', name='Lula Geral',
                                line=dict(color='firebrick', width=1.5, dash='dot')))

        fig.add_annotation(x=list(df[df['lul_ger_2t']>1].sigla)[-1], y=list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        # fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t, x=df[df['bol_ger_2t']>1].sigla, mode='markers', name='Int. voto geral Bolsonaro',
        #                         marker=dict(
        #                         size=5,
        #                         color=df[df['bol_ger_2t']>1].bol_ger_2t, #set color equal to a variable
        #                         colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Bolsonaro Geral',
                                line=dict(color='skyblue', width=1.5, dash='dot')))

        fig.add_annotation(x=list(df[df['bol_ger_2t']>1].sigla)[-1], y=list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))



        ## Intenção de voto Homens
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_h_2t, x=df.sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df.lul_h_2t, #set color equal to a variable
                                colorscale='peach'),legendrank=2))

        fig.add_trace(go.Scatter(y=df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean(), x=df[df['lul_h_2t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5),legendrank=1))

        fig.add_annotation(x=list(df[df['lul_h_2t']>1].sigla)[-1], y=list(df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_h_2t']>1].lul_h_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 5,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_h_2t, x=df.sigla, mode='markers', name='int_vot_bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.bol_h_2t, #set color equal to a variable
                                colorscale='ice'),legendrank=4))

        fig.add_trace(go.Scatter(y=df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean(), x=df[df['bol_h_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5),legendrank=3))

        fig.add_annotation(x=list(df[df['bol_h_2t']>1].sigla)[-1], y=list(df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_h_2t']>1].bol_h_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -15,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos, Nulos 

        fig.add_trace(go.Scatter(y=df.bra_nulo_h_2t, x=df.sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_h_2t, #set color equal to a variable
                                colorscale='gray'),legendrank=6))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_h_2t']>1].bra_nulo_h_2t.rolling(m_m).mean(), x=df[df['bra_nulo_h_2t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='gray', width=2.5),legendrank=5))

        fig.add_annotation(x=list(df[df['bra_nulo_h_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_h_2t']>1].bra_nulo_h_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nulo_h_2t']>1].bra_nulo_h_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=160),
        title=("""
        Média móvel das intenções de voto de <i>homens</i> por candidato à presidência (2º turno)<br>
        """),
            title_xanchor="auto",
            plot_bgcolor='rgb(255, 255, 255)',
            paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br><br><br><br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

        ##pico segunda onda covid
        fig.add_vline(x=str("abr/21_poderdata"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="abr/21_poderdata", y=63,text="Pico<br>2a onda<br>Covid-19",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #moro desiste
        fig.add_vline(x=str("mar/22_poderdata_3"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        fig.add_annotation(x="mar/22_poderdata_3", y=63,text="Moro<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        #dória desiste
        # fig.add_vline(x=str("mai/22_poderdata_2"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        # fig.add_annotation(x="mai/22_poderdata_2", y=63,text="Dória<br>desiste da<br>candidatura",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        # #candidaturas
        fig.add_annotation(x="jul/22_ipespe", y=50,text="Candidatura<br>Lula (PT)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = -30,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="jul/22_ipespe", y=42,text="Candidatura<br>Bolsonaro (PL)",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 60,font=dict(size=10, color="black", family="Arial"))
        #linha inicio campanha
        fig.add_annotation(x="ago/22_fsb", y=61,text="Início da<br>Campanha<br>oficial<br>16/08",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_fsb"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)
        #linha debate
        fig.add_annotation(x="ago/22_ipec_2", y=64,text="1º Debate<br>na TV",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("ago/22_ipec_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        #linha 7 de setembro
        fig.add_annotation(x="set/22_datafolha_2", y=63,text="7 de<br>setembro",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("set/22_datafolha_2"), line_width=.3, line_dash="dot", line_color="black", opacity=.5)
        ##resultado 1o turno
        fig.add_annotation(x="out/22_ipec", y=63,text="<b>Resultado<br>1º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_ipec", y=58,text="Lula = 48,4%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_ipec", y=31,text="Bolsonaro = 43,2%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("out/22_ipec"), line_width=.5, line_dash="dot", line_color="black", opacity=.5)        
        # ##resultado 2o turno
        fig.add_annotation(x="out/22_datafolha_6", y=63,text="<b>Resultado<br>2º turno</b>",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha_6", y=58,text="Lula = 50,9%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="out/22_datafolha_6", y=31,text="Bolsonaro = 49,1%",showarrow=False,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_vline(x=str("out/22_datafolha_6"), line_width=.5, line_dash="dot", line_color="black", opacity=.4)

        fig.update_xaxes(tickangle = 300,rangeslider_visible=False,title_font_family="Arial")

        # Add image
        # fig.add_layout_image(
        #     dict(
        #         source=agre,
        #         xref="paper", yref="paper",
        #         x=.99, y=1.15,
        #         sizex=0.14, sizey=0.14,
        #         xanchor="right", yanchor="bottom"
        #     )
        # )

        st.plotly_chart(fig,use_container_width=True)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color: black; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto por gênero utilizamos {len(df[df['lul_h_2t']>1])} pesquisas eleitorais.</h7><br>
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
            inst2 = st.selectbox('Selecione o instituto de pesquisa:',options=institutos)
        with col1:
            ## drop'  Parda', '  Branca', '  Preta', '  Outras', 
            raça6 = st.selectbox('Escolha o gênero:',options=['  --Selecione uma opção--  ','  Mulheres', '  Homens'])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            

            if raça6 == '  Homens':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                genero_escolhido = 'h'
                genero = 'homens'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{genero_escolhido}_2t'], mode='lines+markers', name=f"Lula - {genero}",
                                        line=dict(color='firebrick', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=1))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{genero_escolhido}_2t'], mode='lines+markers', name=f"Bolsonaro - {genero}",
                                        line=dict(color='royalblue', width=2.5),legendrank=4))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=3))
                
                fig.update_layout(width = 900, height = 700, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=2, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{genero}' por candidato - {inst2.title()} (2º turno)
                        <br>
                        <br>
                        """),
                                        plot_bgcolor='rgb(255, 255, 255)',
                                        paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br>Legenda:<br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])


                # Add image
                # fig.add_layout_image(
                #     dict(
                #         source=agre,
                #         xref="paper", yref="paper",
                #         x=.99, y=1.08,
                #         sizex=0.14, sizey=0.14,
                #         xanchor="right", yanchor="bottom"
                #     )
                # )
                
                st.plotly_chart(fig)


            if raça6 == '  Mulheres':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                genero_escolhido = 'm'
                genero = 'mulheres'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{genero_escolhido}_2t'], mode='lines+markers', name=f"Lula - {genero}",
                                        line=dict(color='firebrick', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'], mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=1))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{genero_escolhido}_2t'], mode='lines+markers', name=f"Bolsonaro - {genero}",
                                        line=dict(color='royalblue', width=2.5),legendrank=4))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'], mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=3))
                
                fig.update_layout(width = 900, height = 700, template = 'plotly_white+xgridoff', margin=dict(r=80, l=80, b=15, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{genero}' por candidato - {inst2.title()} (2º turno)
                        <br>
                        <br>
                        """),
                                        title_xanchor="auto",
                                        plot_bgcolor='rgb(255, 255, 255)',
                                        paper_bgcolor='rgb(255, 255, 255)',
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br><br><br>Legenda:<br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])


                # Add image
                # fig.add_layout_image(
                #     dict(
                #         source=agre,
                #         xref="paper", yref="paper",
                #         x=.99, y=1.08,
                #         sizex=0.14, sizey=0.14,
                #         xanchor="right", yanchor="bottom"
                #     )
                # )
                
                st.plotly_chart(fig)
               
        
        st.markdown(f"""
        <h7 style='text-align: center; color: black; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte de gênero. No entanto, nem todos os institutos coletam tais informações. Assim, se a combinação selecionada retornar apenas os dados de intenção de voto geral, isso significa, que o instituto selecionado não coletou a informação.</h7>
        """, unsafe_allow_html=True)
    st.markdown("---")
    