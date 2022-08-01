from ctypes import alignment
from ctypes.wintypes import RGB
from lib2to3.pgen2.pgen import DFAState
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
     page_title="Agregador de pesquisas eleitorais por religião",
     page_icon="chart_with_upwards_trend",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "##### Cientista de dados: Dirceu André Gerardi. \n **E-mail:** andregerardi3@gmail.com"
     }
 )


## compartilhamento
st.markdown("""
<h8 style='text-align: center; color:#54595F;font-family:Segoe UI'>Compartilhe com</h8><br>
<a href="https://www.facebook.com/sharer/sharer.php?u=https://cebrap.org.br/agregador-de-pesquisas-eleitorais-por-religiao Agregador de Pesquisas Eleitorais por religião" title="Agregador de Pesquisas Eleitorais por religião" rel="nofollow noopener" style="font-size:32px!important;box-shadow:none;display:inline-block;vertical-align:middle"><span class="heateor_sss_svg" style="background-color:#3c589a;width:50px;height:50px;display:inline-block;opacity:1;float:left;font-size:32px;box-shadow:none;display:inline-block;font-size:16px;padding:0 4px;vertical-align:middle;background-repeat:repeat;overflow:hidden;padding:0;cursor:pointer;box-sizing:content-box"><svg style="display:block;" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="-5 -5 42 42"><path d="M17.78 27.5V17.008h3.522l.527-4.09h-4.05v-2.61c0-1.182.33-1.99 2.023-1.99h2.166V4.66c-.375-.05-1.66-.16-3.155-.16-3.123 0-5.26 1.905-5.26 5.405v3.016h-3.53v4.09h3.53V27.5h4.223z" fill="#fff"></path></svg></span></a>
<a href="https://twitter.com/intent/tweet?text=Agregador de Pesquisas Eleitorais por religião&nbsp;&url=https://cebrap.org.br/agregador-de-pesquisas-eleitorais-por-religiao&nbsp;&hashtags=Agregador,religião,eleições2022,datascience" title="Twitter" rel="nofollow noopener" target="_blank" style="font-size:32px!important;box-shadow:none;display:inline-block;vertical-align:middle"><span class="heateor_sss_svg heateor_sss_s__default heateor_sss_s_twitter" style="background-color:#55acee;width:50px;height:50px;display:inline-block;opacity:1;float:left;font-size:32px;box-shadow:none;display:inline-block;font-size:16px;padding:0 4px;vertical-align:middle;background-repeat:repeat;overflow:hidden;padding:0;cursor:pointer;box-sizing:content-box"><svg style="display:block;" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="-4 -4 39 39"><path d="M28 8.557a9.913 9.913 0 0 1-2.828.775 4.93 4.93 0 0 0 2.166-2.725 9.738 9.738 0 0 1-3.13 1.194 4.92 4.92 0 0 0-3.593-1.55 4.924 4.924 0 0 0-4.794 6.049c-4.09-.21-7.72-2.17-10.15-5.15a4.942 4.942 0 0 0-.665 2.477c0 1.71.87 3.214 2.19 4.1a4.968 4.968 0 0 1-2.23-.616v.06c0 2.39 1.7 4.38 3.952 4.83-.414.115-.85.174-1.297.174-.318 0-.626-.03-.928-.086a4.935 4.935 0 0 0 4.6 3.42 9.893 9.893 0 0 1-6.114 2.107c-.398 0-.79-.023-1.175-.068a13.953 13.953 0 0 0 7.55 2.213c9.056 0 14.01-7.507 14.01-14.013 0-.213-.005-.426-.015-.637.96-.695 1.795-1.56 2.455-2.55z" fill="#fff"></path></svg></span></a>
<a href="https://api.whatsapp.com/send?text=Agregador de Pesquisas Eleitorais por religião - https://cebrap.org.br/agregador-de-pesquisas-eleitorais-por-religiao/" title="Whatsapp" rel="nofollow noopener" target="_blank" style="font-size:32px!important;box-shadow:none;display:inline-block;vertical-align:middle"><span class="heateor_sss_svg" style="background-color:#55eb4c;width:50px;height:50px;display:inline-block;opacity:1;float:left;font-size:32px;box-shadow:none;display:inline-block;font-size:16px;padding:0 4px;vertical-align:middle;background-repeat:repeat;overflow:hidden;padding:0;cursor:pointer;box-sizing:content-box"><svg style="display:block;" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="-6 -5 40 40"><path class="heateor_sss_svg_stroke heateor_sss_no_fill" stroke="#fff" stroke-width="2" fill="none" d="M 11.579798566743314 24.396926207859085 A 10 10 0 1 0 6.808479557110079 20.73576436351046"></path><path d="M 7 19 l -1 6 l 6 -1" class="heateor_sss_no_fill heateor_sss_svg_stroke" stroke="#fff" stroke-width="2" fill="none"></path><path d="M 10 10 q -1 8 8 11 c 5 -1 0 -6 -1 -3 q -4 -3 -5 -5 c 4 -2 -1 -5 -1 -4" fill="#fff"></path></svg></span></a></div></div>
<br>
""",unsafe_allow_html=True)

## titulo
st.markdown("""
<br>
<h1 style='text-align: center; color:#303030;font-family:Segoe UI'>Agregador de pesquisas eleitorais por religião</h1>
""", unsafe_allow_html=True)

## subtítulo do cabeçalho
st.markdown("""
<br>
<h4 style='text-align: center; color:#54595F;font-family:Segoe UI'>Consolidação de pesquisas para as eleições presidenciais de 2022</h4>
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

## MÉDIA MÓVEL 7 dias
m_m = 7

## MÉDIA MÓVEL 15 DIAS (EXCLUSIVO PARA O GRÁFICO DE REJEIÇÃO GERAL)
m_m15 = 15

### dados de tempo
end_date = dt.datetime.today() # data atual
start_date = dt.datetime(2022,8,16) # data de oito meses atras

### dados pesquisas
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_excel('resultados_pesquisas_lula_bolsonaro_religião.xlsx')
    return df
df = load_data()

##import image logo
@st.cache(allow_output_mutation=True)
def load_image():
    agre = Image.open('palacio-da-alvorada-interior-black-so-agregador-branco.jpg')
    return agre
agre = load_image()


###############################################################################
## importa e plota o quadro com a lista de pesquisas utilizadas pelo agregador##
################################################################################
st.markdown("---")
with st.container():
    col3,col4,col5 = st.columns([.5,4,.5])
    with col4:
        st.markdown("""
        <br>
        <h4 style='text-align: center; color: #ffffff;font-family:font-family:poppins-sans-serif;background-color: #FA7A35;'><b>Informações sobre o agregador:<b></h4><br>
        """, unsafe_allow_html=True)

        ### primeiro expander, da metodologia
        expander = st.expander('Descubra aqui como o agregador foi construído',)
        expander.markdown(f"""
        <!DOCTYPE html>
        <html>
        <body>

        <p style='text-align: center; font-family:Segoe UI;'><b>Explicação:</b></p>

        <p style='text-align: justify; font-family:Segoe UI;'>1. O banco de dados é atualizado constantemente com informações sobre a intenção de voto e a rejeição dos candidatos por religião.</p>
        <p style='text-align: justify; font-family:Segoe UI;'>2. Os institutos de pesquisa consultados são: { ', '.join(set(df['nome_instituto'].T)).title().replace('Mda','MDA').replace('Fsb','FSB').replace('Idea','Idea Big Data').replace('Voxpopuli','Vox Populi').replace('Prpesquisas','Paraná Pesquisas')};</p>
        <p style='text-align: justify; font-family:Segoe UI;'>3. O agregador de pesquisas por religião compila os dados de levantamentos nacionais realizados pelos institutos, desde janeiro de 2021. Não nos responsabilizamos pelas amostras ou técnicas utilizadas pelos diversos institutos;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>4. Devido à irregularidade na coleta e ao tamanho da amostra, dados referentes a segmentos demograficamente minoritários tal como candomblé/umbanda e outros apresentam margens de erro maiores, uma vez que a amostra destas religiões não é representativa do conjunto da população brasileira. Assim, quando possível, decidiu-se incluí-las na categoria "Outros";</p>
        <p style='text-align: justify; font-family:Segoe UI;'>5. Para a composição do banco de dados são consideradas apenas pesquisas nacionais, bem como informações de Lula, Bolsonaro e Ciro Gomes no primeiro turno das eleições presidenciais e de Lula e Bolsonaro no 2º turno;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>6. Vale destacar que os dados censitários, principais referências para a construção da amostragem das pesquisas, estão defasados. Os valores de amostragem variam conforme os critérios próprios de cada instituto de pesquisa. Os institutos utilizam dados o IBGE de 2010, da PNAD de 2021 e 2022 e do TSE. As informações de corte religioso nem sempre estão disponíveis nas pesquisas compartilhadas publicamente ou não constam nos documentos registrados no sistema <a href="https://www.tse.jus.br/eleicoes/pesquisa-eleitorais/consulta-as-pesquisas-registradas">PesqeEle</a> matido pelo do TSE, dado que não é obrigatório, segundo o artigo 33 da <a href="https://www.tse.jus.br/legislacao/codigo-eleitoral/lei-das-eleicoes/sumario-lei-das-eleicoes-lei-nb0-9.504-de-30-de-setembro-de-1997">Lei nº 9.504/1997</a>. Para termos uma noção do universo amostrado pelos institutos: os <i>católicos</i> variaram entre {int(df['am_cat'].agg('min'))}% e {int(df['am_cat'].agg('max'))}% dos entrevistados; os <i>evangélicos</i>, entre {int(df['am_ev'].agg('min'))}% e {int(df['am_ev'].agg('max'))}%; os <i>espíritas</i>, entre {int(df['am_espi'].agg('min'))}% e {int(df['am_espi'].agg('max'))}%; o <i>candomblé/umbanda</i>, entre {int(df['am_umb_can'].agg('min'))}% e {int(df['am_umb_can'].agg('max'))}%; <i>outras religiões</i>, entre {int(df['am_out'].agg('min'))}% e {int(df['am_out'].agg('max'))}%; os <i>sem religião</i>, entre {int(df['am_non'].agg('min'))}% e {int(df['am_non'].agg('max'))}%; e <i>os ateus</i>, entre {int(df['am_ateu'].agg('min'))}% e {int(df['am_ateu'].agg('max'))}%.</p>
        <p style='text-align: justify; font-family:Segoe UI;'>7. Em relação às pesquisas, no levantamento de dados para o agregador, considerou-se a última data quando os entrevistadores colheram as respostas e não a data da divulgação da pesquisa, que por interesses diversos, podem ser adiadas por semanas;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>8. Partindo da data da última coleta das pesquisas, calculou-se a média móvel de diversas variáveis correspondendo a {m_m} dias. Para o caso da rejeição geral utilizou-se a média móvel de {m_m15} dias;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>9. Para obter a média móvel foram usados dados de uma série temporal e aplicado o seguinte código Python <code>rolling().mean()</code>. Uma explicação detalhada da utilização deste código pode ser <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html">vista aqui</a>;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>10. Ao calcular a média móvel de {m_m} dias, por exemplo, os {m_m} primeiros resultados são omitidos da série temporal e não aparecem nos gráficos. O objetivo principal da aplicação deste método é reduzir as oscilações no intuito de deixar as linhas dos gráficos mais fluídas. Exitem outras técnicas estatíticas para a redução do ruído dos dados da série temporal, tais como <i>weighted moving average, kernel smoother</i>, entre outras;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>11. O resumo das médias móveis apresentado no primeiro e no segundo turnos considera e apresenta o último valor da média obtida para cada candidato. O dado é atualizado automaticamente à medida que novas pesquisas são inseridas no banco de dados;</p>
        <p style='text-align: justify; font-family:Segoe UI;'>12. Para deixar os gráficos limpos optou-se por não inserir a margem de erro na linha da média móvel. Nos recortes por religião a margem de erro varia entre 2% até 8,5%, de acordo com os institutos. Uma lista com as informações amostrais de cada pesquisa, incluindo a margem de erro, poderá ser obtida no item "pesquisas eleitorais utilizadas";</p>
        <p style='text-align: justify; font-family:Segoe UI;'>13. As imagens dos candidatos utilizadas provêm das seguintes fontes: <a href="https://oglobo.globo.com/epoca/o-que-dizem-os-autores-dos-programas-dos-presidenciaveis-sobre-combate-as-mudancas-climaticas-23128520">Ciro Gomes</a>, <a href="https://www.dw.com/pt-br/o-brasil-na-imprensa-alem%C3%A3-29-05/a-48968730/">Lula</a>, <a href="https://www.poder360.com.br/poderdata/poderdata-lula-tem-50-contra-40-de-bolsonaro-no-2o-turno/">Bolsonaro</a>.</p>

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
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Abrangencia das pesquisas:</h6> <p style='text-align: center';>Nacional</p>
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Institutos analisados:</h6> <p style='text-align: center';>{', '.join(set(df['nome_instituto'].T)).title()}</p>
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Institutos por tipo de sondagem:</h6> <p style='text-align: center';>
                <i>Telefone:</i> {', '.join(set(df[df['tipo_coleta']=='telefone'].nome_instituto)).title().replace('Mda','MDA').replace('Fsb','FSB').replace('Idea','Idea Big Data').replace('Voxpopuli','Vox Populi').replace('Prpesquisas','Paraná Pesquisas')}<br>
                <br><i>Presencial:</i> {', '.join(set(df[df['tipo_coleta']=='presencial'].nome_instituto)).title().replace('Mda','MDA').replace('Fsb','FSB').replace('Idea','Idea Big Data').replace('Voxpopuli','Vox Populi').replace('Prpesquisas','Paraná Pesquisas')} ;</p>
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Número de pesquisas segundo método de coleta:</h6><p style='text-align: center';>
                Telefone: {df[df['tipo_coleta']=='telefone'].tipo_coleta.value_counts()[0]}
                <br>Presencial: {df[df['tipo_coleta']=='presencial'].tipo_coleta.value_counts()[0]}</p>
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Contador de pesquisas para dados gerais:</h6> 
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            1º turno: {len(df[df['lul_ger_1t']>=1])}<br>
            2º turno: {len(df[df['lul_ger_2t']>=1])}</p>
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Contador de pesquisas com perguntas sobre religião:</h6> 
            <p style='color:#000000;font-weight:700;font-size:18px;text-align: center';>
            1º turno: {len(df[df['lul_cat_1t']>=1])}<br>
            2º turno: {len(df[df['lul_cat_2t']>=1])}</p>
            <h6 style='text-align: center; color: rgb(37, 117, 232);font-family:Segoe UI;'>Total de pesquisas com amostra sobre religião:</h6><p style='text-align: center';>
            Católicos e evangélicos: {len(df[df['lul_cat_1t']>=1])}
            <br>Espíritas: {len(df[df['lul_espi_1t']>=1])}
            <br>Outras religiões: {len(df[df['lul_out_1t']>=1])}
            <br>Sem religião: {len(df[df['lul_non_1t']>=1])}
            </p>
        """, unsafe_allow_html=True)

        ### Como citar o agregador ####
    with col2:
        expander2 = st.expander("Veja como citar o agregador")
        expander2.markdown(f"""
        <p style='text-align: center; font-family:Segoe UI;'>GERARDI, Dirceu André; ALMEIDA, Ronaldo de. <b>Agregador de pesquisas eleitorais por religião</b>: consolidação de dados de pesquisas eleitorais com recorte religioso às eleições presidenciais de 2022. APP versão 1.0. São Paulo, 2022. Disponível em: https://cebrap.org.br/projetos/. Acesso em: 00/00/000.</p>
        """, unsafe_allow_html=True)

    with col3:
        expander5 = st.expander("Sobre nós")
        expander5.markdown(f"""
        <h6 style='text-align: center; color: #41AF50;'>Projeto vinclulado ao <br> Núcleo de Religiões no Mundo Contemporâneo - Cebrap</h6>
        <h6 style='text-align: center; color: #54595F;'>Coordenação:</h6><p style='text-align: center;'>Dirceu André Gerardi<br>(LabDados|FGV Direito SP/CEBRAP)<br><a href="mailto: andregerardi3@gmail.com">email<br></a><br>Ronaldo de Almeida<br>(UNICAMP/CEBRAP/LAR)<br><a href="mailto: ronaldormalmeida@gmail.com">email</a></p></p>
        """, unsafe_allow_html=True)
    st.markdown("---")

########################################################################
#### seletor para escolher o perído do primeiro ou do segundo turno#####
########################################################################

with st.container():
    col3,col4,col5 = st.columns([.5,1.5,.5])
    with col4:
        st.markdown("<h4 style='text-align: center; color: #ffffff; font-family:font-family:poppins-sans-serif; background-color: rgb(0, 165, 200, 100);'>Selecione o turno da eleição para visualizar os dados:</h4>", unsafe_allow_html=True)
        options_turn = st.selectbox('',options=['--clique para selecionar--','Primeiro Turno', 'Segundo Turno'])
st.markdown("---")

########################
### primeiro turno #####
########################

if options_turn == 'Primeiro Turno':

    ######################
    ###compartilhamento###
    ######################

    st.markdown(f"""
        <h2 style='text-align: center; color: #303030; font-family:tahoma; text-rendering: optimizelegibility;'>Primeiro Turno</h2>
        <br>
        """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
        <h3 style='text-align: center; color: #303030; font-family:segoe UI; text-rendering: optimizelegibility;background-color: #FFD662;'>1. Intenção de voto:</h3>
        """, unsafe_allow_html=True)
    st.markdown("---")

    ############################################
    ## média movel dos candidatos por segmento##
    ############################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'>Resumo - intenção de voto geral e por religião segundo candidato:</h3><br>
        """, unsafe_allow_html=True)

        int_vot_lula = st.checkbox('Lula')

        if int_vot_lula:

            ## coluna 1
            lul = Image.open('lula_perfil.jpg')
            col0, col, col1, col2, col3, col4, col5 = st.columns(7)
            col0.image(lul,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Católicos", value=f"{round(list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}")
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(round(list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            col3.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1)-round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            col4.metric(label="Outros", value=f"{round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")
            col5.metric(label="Sem Religião", value=f"{round(list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1],1)}%") # delta=f"{round(list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1)}")
            #col5.metric(label="Rejeição", value=f"{round(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            
            ## coluna 2agre
            #col4, col5, col6, col7, col8 = st.columns(5)
            #col4.metric(label="",value="")
            #col5.metric(label="Outros", value=f"{round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1)}%") #delta=f"{round(round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")
            #col6.metric(label="Ateu", value=f"{round(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            #col7.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1)-round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            #col8.metric(label="Umbanda/Candomblé", value=f"{round(list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            ## info
            st.markdown("---")

        int_vot_bolsonaro = st.checkbox('Bolsonaro')

        if int_vot_bolsonaro:

            ## coluna 1
            bol = Image.open('bolso_image.jpeg')
            col0, col, col1, col2, col3, col4, col5 = st.columns(7)
            col0.image(bol,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ger_1t']>1].lul_ger_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Católicos", value=f"{round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1],1)}%")
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            col3.metric(label="Espíritas", value=f"{round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            col4.metric(label="Outros", value=f"{round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_out_1t']>1].lul_out_1t.rolling(m_m).mean())[-1],1),1)}")
            col5.metric(label="Sem Religião", value=f"{round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1],1)}")
            #col6.metric(label="Rejeição", value=f"{round(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            #col6.metric(label="Gestão:'ruim/péssima'", value=f"{round(list(df[df['ava_gov_bol_GERAL']>1].ava_gov_bol_GERAL.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")

            ## coluna 2
            #col4, col5, col6, col7, col8 = st.columns(5)
            #col4.metric(label="",value="")
            #col3.metric(label="Espíritas", value=f"{round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            #col5.metric(label="Umbanda/Candomblé", value=f"{round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            #col6.metric(label="Ateu", value=f"{round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            ## info
            st.markdown("---")

        int_vot_ciro = st.checkbox('Ciro Gomes')

        if int_vot_ciro:

            ## coluna 1
            ciro = Image.open('ciro_perfil.jpg')
            col0, col, col1, col2, col3, col4, col5 = st.columns(7)
            col0.image(ciro,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_ger_1t']>1].ciro_ger_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_1t']>1].bol_ger_1t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Católicos", value=f"{round(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],1)}%")
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],1),1)}")
            col3.metric(label="Espíritas", value=f"{round(list(df[df['ciro_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            col4.metric(label="Outros", value=f"{round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")
            col5.metric(label="Sem Religião", value=f"{round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1),1)}")
            #col5.metric(label="Rejeição", value=f"{round(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1],1),1)}")
            ## coluna 2
            #col4, col5, col6, col7, col8 = st.columns(5)
            #col4.metric(label="",value="")
            #col5.metric(label="Umbanda/Candomblé", value=f"{round(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],1),1)}")
            #col6.metric(label="Ateu", value=f"{round(list(df[df['ciro_ateu_1t']>=1].ciro_ateu_1t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],1),1)}")
            #col7.metric(label="Sem Religião", value=f"{round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],1),1)}")
            #col8.metric(label="Outros", value=f"{round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],1),1)}")
            #col3.metric(label="Espíritas", value=f"{round(list(df[df['ciro_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],1),1)}")


        st.markdown(f"""
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado para o cálculo: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no resumo correspondem a última média da série temporal registrada no dia <i>{list(df.data)[-1].strftime(format='%d-%m-%Y')}</i></h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)

    st.markdown("---")

    #####################################################
    ## gráfico intenção de voto geral - primeiro turno###
    #####################################################


    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto geral:</h3><br>
        """, unsafe_allow_html=True)

        int_vote_med_move = st.checkbox('Selecione para visualizar o gráfico da intenção de voto geral')

        if int_vote_med_move:

            ##import image

            fig = go.Figure()

            ## lula
            fig.add_trace(go.Scatter(y=df.lul_ger_1t, x=df.sigla, mode='markers', name='Int. voto Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df.lul_ger_1t.rolling(m_m).mean(), x=df.sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=list(df.lul_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df.lul_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))


            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df.bol_ger_1t, x=df.sigla, mode='markers', name='Int. voto Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_ger_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df.bol_ger_1t.rolling(m_m).mean(), x=df.sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=list(df.bol_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df.bol_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df.ciro_ger_1t, x=df.sigla, mode='markers', name='Int. voto Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_ger_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df.ciro_ger_1t.rolling(m_m).mean(), x=df.sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=list(df.ciro_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df.ciro_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 20,
                        font=dict(size=20, color="black", family="Arial"))


            # ## Brancos e Nulos e não sabe e não respondeu

            # fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_1t, x=df.sigla, mode='markers', name='brancos_nulos_ns_nr',
            #                         marker=dict(
            #                         size=5,
            #                         color=df.bra_nul_ns_nr_ger_1t, #set color equal to a variable
            #                         colorscale='Greys')))

            # fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean(), x=df.sigla, mode='lines', name='Brancos, nulos, NS e NR',
            #                         line=dict(color='grey', width=2.5)))

            # fig.add_annotation(x=list(df.sigla)[-1], y=list(df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1] ,text=f"{int(list(df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1])}%",
            #             showarrow=True,
            #             arrowhead=1,
            #             ax = 40, ay = -8,
            #             font=dict(size=20, color="black", family="Arial"))

            ## Brancos e Nulos, NS e NR

            fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_1t, x=df.sigla, mode='markers', name='Brancos, nulos NS e NR',
                                    marker=dict(
                                    size=5,
                                    color=df.bra_nul_ns_nr_ger_1t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean(), x=df.sigla, mode='lines', name='Brancos, nulos NS e NR',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df.sigla)[-1], y=list(df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1],text=f"{int(list(df.bra_nul_ns_nr_ger_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -0.5,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(autosize=True, width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=160),
            title="<i>Média móvel das intenções de voto de candidatos à presidência (1º turno)<i>",
            title_xanchor="auto",
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend_title_text='<br><br>',
                            legend=dict(
                orientation="v",
                font_family="arial",))

            fig.add_annotation(x="mar/22_poderdata_3", y=29,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=32,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="jun/22_fsb_2", y=31,text="Datena<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            fig.update_yaxes(range=[0,60]) ## exibe o intervalo de y a ser exibido no gráfico

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.05,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.87, y=1.05,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: *Método utilizado:* média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df.data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)
    st.markdown("---")

    ###################################
    ## Intenção de voto por religião ##
    ###################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por religião:</h3><br>
        """, unsafe_allow_html=True)
        ## opções retiradas 'Umbanda/Candomblé', 'Ateu',
        relig = st.selectbox('Selecione a religião:',options=['--Escolha a opção--','Católica', 'Evangélica', 'Espírita', 'Sem Religião', 'Outras Religiosidades'])

        if relig == 'Católica':

            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_cat_1t']>1].lul_cat_1t, x=df[df['lul_cat_1t']>1].sigla, mode='markers', name='Int. voto Lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_cat_1t']>1].lul_cat_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean(), x=df[df['bol_cat_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_cat_1t']>1].sigla)[-1], y=list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_cat_1t']>1].lul_cat_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_cat_1t']>1].bol_cat_1t, x=df[df['bol_cat_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_cat_1t']>1].lul_cat_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean(), x=df[df['bol_cat_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_cat_1t']>1].sigla)[-1], y=list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_cat_1t']>1].bol_cat_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df[df['ciro_cat_1t']>1].ciro_cat_1t, x=df[df['ciro_cat_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_cat_1t']>1].ciro_cat_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean(), x=df[df['ciro_cat_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_cat_1t']>1].sigla)[-1], y=list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_cat_1t']>1].ciro_cat_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -8,
                        font=dict(size=20, color="black", family="Arial"))

            ## Brancos e Nulos

            fig.add_trace(go.Scatter(y=df[df['bra_nulo_cat_1t']>1].bra_nulo_cat_1t, x=df[df['bra_nulo_cat_1t']>1].sigla, mode='markers', name='Brancos e Nulos',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bra_nulo_cat_1t']>1].bra_nulo_cat_1t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nulo_cat_1t']>1].bra_nulo_cat_1t.rolling(m_m).mean(), x=df[df['bra_nulo_cat_1t']>1].sigla, mode='lines', name='Brancos, nulos',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df[df['bra_nulo_cat_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_cat_1t']>1].bra_nulo_cat_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_cat_1t']>1].bra_nulo_cat_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 20,
                        font=dict(size=20, color="black", family="Arial"))


            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=110),
            title=("""
            <i>Média móvel das intenções de voto de católicos por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            legend_title_text='<br><br>',
                            font=dict(family="arial",size=13),
                            legend=dict(
                orientation="v",
                font_family="arial"))

            fig.add_annotation(x="mar/22_poderdata_3", y=25,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="jun/22_datafolha", y=26,text="Datena<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            fig.update_yaxes(range=[0,65]) ## exibe o intervalo de y a ser exibido no gráfico

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.08,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)

            ## info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais e {len(df[df['lul_cat_1t']>1])} para os católicos.</h7><br>
            """, unsafe_allow_html=True)

        if relig == 'Evangélica':
            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_ev_1t']>1].lul_ev_1t, x=df[df['lul_ev_1t']>1].sigla, mode='markers', name='Int. voto Lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_ev_1t']>1].lul_ev_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean(), x=df[df['bol_ev_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ev_1t']>1].sigla)[-1], y=list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ev_1t']>1].lul_ev_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))
            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_ev_1t']>1].bol_ev_1t, x=df[df['bol_ev_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_ev_1t']>1].bol_ev_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean(), x=df[df['bol_ev_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ev_1t']>1].sigla)[-1], y=list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ev_1t']>1].bol_ev_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))
            ## Ciro
            fig.add_trace(go.Scatter(y=df[df['ciro_ev_1t']>1].ciro_ev_1t, x=df[df['ciro_ev_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_ev_1t']>1].ciro_ev_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean(), x=df[df['ciro_ev_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_ev_1t']>1].sigla)[-1], y=list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_ev_1t']>1].ciro_ev_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 20,
                        font=dict(size=20, color="black", family="Arial"))

            ## Brancos e Nulos

            fig.add_trace(go.Scatter(y=df[df['bra_nulo_ev_1t']>1].bra_nulo_ev_1t, x=df[df['bra_nulo_ev_1t']>1].sigla, mode='markers', name='Brancos e nulos',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bra_nulo_ev_1t']>1].bra_nulo_ev_1t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nulo_ev_1t']>1].bra_nulo_ev_1t.rolling(m_m).mean(), x=df[df['bra_nulo_ev_1t']>1].sigla, mode='lines', name='Brancos e nulos',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df[df['bra_nulo_ev_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_ev_1t']>1].bra_nulo_ev_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_ev_1t']>1].bra_nulo_ev_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -8,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=110),
            title=("""
            <i>Média móvel das intenções de voto de evangélicos por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            legend_title_text='<br><br>',
                            font=dict(family="arial",size=13),
                            legend=dict(
                orientation="v",
                font_family="arial",))

            fig.add_annotation(x="mar/22_poderdata_3", y=28,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=28,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="jun/22_datafolha", y=27,text="Datena<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 300,rangeslider_visible=False,title_font_family="Arial")

            fig.update_yaxes(range=[0,60]) ## exibe o intervalo de y a ser exibido no gráfico

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.08,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)

            ## info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais e {len(df[df['lul_ev_1t']>1])} para os evangélicos.</h7><br>
            """, unsafe_allow_html=True)

        if relig == 'Espírita':
            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df[df['lul_espi_1t']>1].lul_espi_1t, x=df[df['lul_espi_1t']>1].sigla, mode='markers', name='Int. voto Lula',
                                    marker=dict(
                                    size=5,
                                    color=df[df['lul_espi_1t']>1].lul_espi_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean(), x=df[df['bol_espi_1t']>1].sigla,mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_espi_1t']>1].sigla)[-1], y=list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_espi_1t']>1].lul_espi_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df[df['bol_espi_1t']>1].bol_espi_1t, x=df[df['bol_espi_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bol_espi_1t']>1].bol_espi_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean(), x=df[df['bol_espi_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_espi_1t']>1].sigla)[-1], y=list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_espi_1t']>1].bol_espi_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                            ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Ciro

            fig.add_trace(go.Scatter(y=df[df['ciro_espi_1t']>1].ciro_espi_1t, x=df[df['ciro_espi_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_espi_1t']>1].ciro_espi_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean(), x=df[df['ciro_espi_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_espi_1t']>1].sigla)[-1], y=list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_espi_1t']>1].ciro_espi_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -8,
                        font=dict(size=20, color="black", family="Arial"))

            # Brancos e Nulos
            ## inseri o filtro do lula na barra x para poder incluir o valor tipo padrão

            fig.add_trace(go.Scatter(y=df[df['bra_nulo_espi_1t']>1].bra_nulo_espi_1t, x=df[df['bra_nulo_espi_1t']>1].sigla, mode='markers', name='Brancos e nulos',
                                    marker=dict(
                                    size=5,
                                    color=df[df['bra_nulo_espi_1t']>1].bra_nulo_espi_1t, #set color equal to a variable
                                    colorscale='Greys')))

            fig.add_trace(go.Scatter(y=df[df['bra_nulo_espi_1t']>1].bra_nulo_espi_1t.rolling(m_m).mean(), x=df[df['bra_nulo_espi_1t']>1].sigla, mode='lines', name='Brancos e nulos',
                                    line=dict(color='grey', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_espi_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_espi_1t']>1].bra_nulo_espi_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_espi_1t']>1].bra_nulo_espi_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 20,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=110),
            title=("""
            <i>Média móvel das intenções de voto de espíritas por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            legend_title_text='<br><br>',
                            font=dict(family="arial",size=13),
                            legend=dict(
                orientation="v",
                font_family="arial",))

            fig.add_annotation(x="mar/22_poderdata_3", y=28,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=22,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="jun/22_poderdata", y=22,text="Datena<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.08,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)

            ## info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais e {len(df[df['lul_espi_1t']>1])} para os espíritas.</h7><br>
            """, unsafe_allow_html=True)


    # if relig == 'Umbanda/Candomblé':

    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_umb_can_1t']>1].lul_umb_can_1t, x=df[df['lul_umb_can_1t']>1].data, mode='markers', name='int_vot_umb_can_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_umb_can_1t']>1].lul_umb_can_1t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean(), x=df[df['bol_umb_can_1t']>1].data,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_umb_can_1t']>1].data)[-1], y=list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_umb_can_1t']>1].lul_umb_can_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_umb_can_1t']>1].bol_umb_can_1t, x=df[df['bol_umb_can_1t']>1].data, mode='markers', name='int_vot_umb_can_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_umb_can_1t']>1].lul_umb_can_1t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean(), x=df[df['bol_umb_can_1t']>1].data,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_umb_can_1t']>1].data)[-1], y=list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_umb_can_1t']>1].bol_umb_can_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Ciro

    #     fig.add_trace(go.Scatter(y=df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t, x=df[df['ciro_umb_can_1t']>1].data, mode='markers', name='int_vot_umb_can_ciro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t, #set color equal to a variable
    #                             colorscale='Greens')))

    #     fig.add_trace(go.Scatter(y=df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean(), x=df[df['ciro_umb_can_1t']>1].data, mode='lines', name='Ciro Gomes',
    #                             line=dict(color='seagreen', width=2.5)))

    #     fig.add_annotation(x=list(df[df['ciro_umb_can_1t']>1].data)[-1], y=list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_umb_can_1t']>1].ciro_umb_can_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'none',
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     legend=dict(
    #         yanchor="auto",
    #         y=1.1,
    #         xanchor="auto",
    #         x=0.5,
    #         orientation="h"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
    #     st.plotly_chart(fig,use_container_width=True)

    # if relig == 'Ateu':
    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_ateu_1t']>1].lul_ateu_1t, x=df[df['lul_ateu_1t']>1].data, mode='markers', name='int_vot_ateu_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_ateu_1t']>1].lul_ateu_1t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean(), x=df[df['bol_ateu_1t']>1].data,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_ateu_1t']>1].data)[-1], y=list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ateu_1t']>1].lul_ateu_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                   #  ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_ateu_1t']>1].bol_ateu_1t, x=df[df['bol_ateu_1t']>1].data, mode='markers', name='int_vot_ateu_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_ateu_1t']>1].lul_ateu_1t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean(), x=df[df['bol_ateu_1t']>1].data,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_ateu_1t']>1].data)[-1], y=list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ateu_1t']>1].bol_ateu_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Ciro

    #     """fig.add_trace(go.Scatter(y=df[df['ciro_ateu_1t']>1].ciro_ateu_1t, x=df[df['ciro_ateu_1t']>1].data, mode='markers', name='int_vot_ateu_ciro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['ciro_ateu_1t']>1].ciro_ateu_1t, #set color equal to a variable
    #                             colorscale='Greens')))

    #     fig.add_trace(go.Scatter(y=df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean(), x=df[df['ciro_ateu_1t']>1].data, mode='lines', name='Ciro Gomes',
    #                             line=dict(color='seagreen', width=2.5)))

    #     fig.add_annotation(x=list(df[df['ciro_ateu_1t']>1].data)[-1], y=list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_ateu_1t']>1].ciro_ateu_1t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                   #  ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))"""

    #     fig.update_layout(width = 1000, height = 800, template = 'none',
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     legend=dict(
    #         yanchor="auto",
    #         y=1.1,
    #         xanchor="auto",
    #         x=0.5,
    #         orientation="h"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
    #     st.plotly_chart(fig,use_container_width=True)

    if relig == 'Sem Religião':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_non_1t']>1].lul_non_1t, x=df[df['lul_non_1t']>1].sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df[df['lul_non_1t']>1].lul_non_1t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean(), x=df[df['bol_non_1t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_non_1t']>1].sigla)[-1], y=list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_non_1t']>1].lul_non_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df[df['bol_non_1t']>1].bol_non_1t, x=df[df['bol_non_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_non_1t']>1].bol_non_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean(), x=df[df['bol_non_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_non_1t']>1].sigla)[-1], y=list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_non_1t']>1].bol_non_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro

        fig.add_trace(go.Scatter(y=df[df['ciro_non_1t']>1].ciro_non_1t, x=df[df['ciro_non_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_non_1t']>1].ciro_non_1t, #set color equal to a variable
                                colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean(), x=df[df['ciro_non_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_non_1t']>1].sigla)[-1], y=list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_non_1t']>1].ciro_non_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos e Nulos

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_non_1t']>1].bra_nulo_non_1t, x=df[df['bra_nulo_non_1t']>1].sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df[df['bra_nulo_non_1t']>1].bra_nulo_non_1t, #set color equal to a variable
                                colorscale='Greys')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_non_1t']>1].bra_nulo_non_1t.rolling(m_m).mean(), x=df[df['bra_nulo_non_1t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='grey', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_non_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_non_1t']>1].bra_nulo_non_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_non_1t']>1].bra_nulo_non_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=110),
        title=("""
        <i>Média móvel das intenções de voto dos sem religião por candidato à presidência (1º turno)<i><br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        legend_title_text='<br><br>',
                        font=dict(family="arial",size=13),
                        legend=dict(
            orientation="v",
            font_family="arial",))

        fig.add_annotation(x="mar/22_poderdata_3", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_poderdata_2", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        # Add image
        fig.add_layout_image(
            dict(
                source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                xref="paper", yref="paper",
                x=.99, y=1.02,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.08,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig,use_container_width=True)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais e {len(df[df['lul_non_1t']>1])} para sem religião.</h7><br>
        """, unsafe_allow_html=True)

    if relig == 'Outras Religiosidades':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df[df['lul_out_1t']>1].lul_out_1t, x=df[df['lul_out_1t']>1].sigla, mode='markers', name='Int. voto Lula',
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
        fig.add_trace(go.Scatter(y=df[df['bol_out_1t']>1].bol_out_1t, x=df[df['bol_out_1t']>1].sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df[df['bol_out_1t']>1].bol_out_1t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean(), x=df[df['bol_out_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_out_1t']>1].sigla)[-1], y=list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_out_1t']>1].bol_out_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Ciro

        fig.add_trace(go.Scatter(y=df[df['ciro_out_1t']>1].ciro_out_1t, x=df[df['ciro_out_1t']>1].sigla, mode='markers', name='Int. voto Ciro',
                                marker=dict(
                                size=5,
                                color=df[df['ciro_out_1t']>1].ciro_out_1t, #set color equal to a variable
                                colorscale='Greens')))

        fig.add_trace(go.Scatter(y=df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean(), x=df[df['ciro_out_1t']>1].sigla, mode='lines', name='Ciro Gomes',
                                line=dict(color='seagreen', width=2.5)))

        fig.add_annotation(x=list(df[df['ciro_out_1t']>1].sigla)[-1], y=list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_out_1t']>1].ciro_out_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos e Nulos

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_out_1t']>1].bra_nulo_out_1t, x=df[df['bra_nulo_out_1t']>1].sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df[df['bra_nulo_out_1t']>1].bra_nulo_out_1t, #set color equal to a variable
                                colorscale='Greys')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_out_1t']>1].bra_nulo_out_1t.rolling(m_m).mean(), x=df[df['bra_nulo_out_1t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='grey', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_out_1t']>1].sigla)[-1], y=list(df[df['bra_nulo_out_1t']>1].bra_nulo_out_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bra_nulo_out_1t']>1].bra_nulo_out_1t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 20,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=110),
        title=("""
        <i>Média móvel das intenções de voto de outras religiões por candidato à presidência (1º turno)<i><br>
        """),
                        xaxis_title='Mês, ano e instituto de pesquisa',
                        yaxis_title='Intenção de voto (%)',
                        legend_title_text='<br><br>',
                        font=dict(family="arial",size=13),
                        legend=dict(
            orientation="v",
            font_family="arial"))

        fig.add_annotation(x="mar/22_futura", y=20,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
        fig.add_annotation(x="mai/22_futura", y=20,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

        # Add image
        fig.add_layout_image(
            dict(
                source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                xref="paper", yref="paper",
                x=.99, y=1.02,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.08,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )

        st.plotly_chart(fig,use_container_width=True)

        ## info
        st.markdown(f"""
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Para o cálculo da média móvel da intenção de voto geral utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais e {len(df[df['lul_out_1t']>1])} para outras religiosidades.</h7><br>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    #####################################
    ### dados por instituto de pesquisa##
    #####################################

    institutos = list(set(df['nome_instituto']))
    institutos.insert(0, '--Escolha o instituto--')

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por religião e candidato segundo instituto de pesquisa: </h3><br>
        """, unsafe_allow_html=True)

        col, col1 = st.columns(2)
        with col:
            inst = st.selectbox('Selecione o instituto de pesquisa:',options=institutos)
        with col1:
            ##dados retirados 'Espírita', 'Umbanda/Candomblé', 'Ateu',
            rel = st.selectbox('Escolha a religião:',options=['--Escolha a religião--','Católica', 'Evangélica', 'Espírita', 'Sem Religião', 'Outras Religiosidades'])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            if rel == 'Católica':
                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'cat'
                rel = 'católicos'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)

            if rel == 'Evangélica':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'ev'
                rel = 'evangélicos'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)

            if rel == 'Espírita':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'espi'
                rel = 'espíritas'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="v",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            if rel == 'Sem Religião':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'non'
                rel = 'sem religião'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            if rel == 'Outras Religiosidades':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'out'
                rel = 'outras religiões'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 800, template = 'plotly', margin=dict(r=70, l=80, b=4, t=160),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel}' por candidato segundo inst. '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.13,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,60])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=1.05, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=1.05, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            
            # if rel == 'Umbanda/Candomblé':

            #     fonte = df.query(f"nome_instituto =='{inst}'")
            #     religi_escolhida = 'umb_can'
            #     rel = 'umbanda e candomblé'

            #     fig = go.Figure()
            #     ##lula
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
            #                             line=dict(color='firebrick', width=2.5),legendrank=1))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
            #                             line=dict(color='firebrick', width=1, dash='dot')))
            #     ##bolsonaro
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
            #                             line=dict(color='royalblue', width=2.5),legendrank=2))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
            #                             line=dict(color='royalblue', width=1, dash='dot')))
            #     ##ciro gomes
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
            #                             line=dict(color='green', width=2.5),legendrank=3))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
            #                             line=dict(color='green', width=1, dash='dot')))

            #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            #             title=(f"""
            #             Intenção de voto 'geral' de adeptos da '{rel}' por candidato segundo '{inst.title()}' (1º turno)
            #             <br>
            #             <br>
            #             """),
            #                             xaxis_title='Mês, ano e instituto de pesquisa',
            #                             yaxis_title='Intenção de voto (%)',
            #                             font=dict(family="arial",size=13),
            #                             legend=dict(
            #                 yanchor="auto",
            #                 y=1.15,
            #                 xanchor="auto",
            #                 x=0.4,
            #                 orientation="h",
            #                 font_family="arial",))
            #     fig.update_xaxes(tickangle = 300,title_font_family="arial")
            #     fig.update_yaxes(range=[0,90])

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
            #             xref="paper", yref="paper",
            #             x=.99, y=1.03,
            #             sizex=0.1, sizey=0.1,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source=agre,
            #             xref="paper", yref="paper",
            #             x=.99, y=1.08,
            #             sizex=0.12, sizey=0.12,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )
                
            #     st.plotly_chart(fig,use_container_width=True)
            

            # if rel == 'Ateu':

            #     fonte = df.query(f"nome_instituto =='{inst}'")
            #     religi_escolhida = 'ateu'
            #     rel = 'ateus'

            #     fig = go.Figure()
            #     ##lula
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
            #                             line=dict(color='firebrick', width=2.5),legendrank=1))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
            #                             line=dict(color='firebrick', width=1, dash='dot')))
            #     ##bolsonaro
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
            #                             line=dict(color='royalblue', width=2.5),legendrank=2))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
            #                             line=dict(color='royalblue', width=1, dash='dot')))
            #     ##ciro gomes
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
            #                             line=dict(color='green', width=2.5),legendrank=3))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
            #                             line=dict(color='green', width=1, dash='dot')))

            #     fig.update_layout(width = 810, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            #             title=(f"""
            #             Intenção de voto 'geral' de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
            #             <br>
            #             <br>
            #             """),
            #                             xaxis_title='Mês, ano e instituto de pesquisa',
            #                             yaxis_title='Intenção de voto (%)',
            #                             font=dict(family="arial",size=13),
            #                             legend=dict(
            #                 yanchor="auto",
            #                 y=1.15,
            #                 xanchor="auto",
            #                 x=0.4,
            #                 orientation="h",
            #                 font_family="arial",))
            #     fig.update_xaxes(tickangle = 300,title_font_family="arial")
            #     fig.update_yaxes(range=[-0.5,95])

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
            #             xref="paper", yref="paper",
            #             x=1.05, y=1.03,
            #             sizex=0.1, sizey=0.1,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source=agre,
            #             xref="paper", yref="paper",
            #             x=1.05, y=1.08,
            #             sizex=0.12, sizey=0.12,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )
                
            #     st.plotly_chart(fig,use_container_width=True)
                

        st.markdown(f"""
        <h7 style='text-align: center; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte religioso. Em alguns casos os institutos não coletam tais informações.</h7>
        <h7 style='text-align: center; color:#606060;font-family:arial'>Nota 2: Os gráficos com linhas descontinuadas indicam que o instituto não coletou a informação em determinada pesquisa. Um exemplo pode ser visto a partir da combinação "Paraná Pesquisas" e "católicos".</h7>
        """, unsafe_allow_html=True)
    st.markdown("---")


###########################
##rejeição primeiro turno##
###########################

    st.markdown(f"""
        <h3 style='text-align: center; color: #303030; font-family:segoe UI; text-rendering: optimizelegibility;background-color: #FFD662;'>2. Rejeição</h3>
        """, unsafe_allow_html=True)
    st.markdown("---")


    ####################
    ##resumo rejeição###
    ####################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #EAE6DA;'>
        Resumo - Rejeição geral e por religião segundo candidato:</h3><br>
        """, unsafe_allow_html=True)

        rej_lula = st.checkbox('Lula ')

        if rej_lula:

            ## coluna 1
            lul = Image.open('lula_perfil.jpg')
            col0, col, col1, col2, col3, col4 = st.columns(6)
            col0.image(lul,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col1.metric(label="Católicos", value=f"{round(list(df[df['lul_cat_rej_1t']>1].lul_cat_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['lul_ev_rej_1t']>1].lul_ev_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col3.metric(label="Outros", value=f"{round(list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col4.metric(label="Sem Religião", value=f"{round(list(df[df['lul_non_rej_1t']>1].lul_non_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            #col3.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_rej_1t']>1].lul_espi_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            st.markdown("---")

        rej_bolsonaro = st.checkbox('Bolsonaro ')

        if rej_bolsonaro:

            ## coluna 1
            bol = Image.open('bolso_image.jpeg')
            col0,col, col1, col2, col3, col4 = st.columns(6)
            col0.image(bol,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col1.metric(label="Católicos", value=f"{round(list(df[df['bol_cat_rej_1t']>1].bol_cat_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['bol_ev_rej_1t']>1].bol_ev_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col3.metric(label="Outros", value=f"{round(list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col4.metric(label="Sem Religião", value=f"{round(list(df[df['bol_non_rej_1t']>1].bol_non_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            #col3.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_rej_1t']>1].lul_espi_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            st.markdown("---")

        rej_ciro = st.checkbox('Ciro Gomes ')

        if rej_ciro:

            ## coluna 1
            ciro = Image.open('ciro_perfil.jpg')
            col0,col, col1, col2, col3, col4 = st.columns(6)
            col0.image(ciro,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col1.metric(label="Católicos", value=f"{round(list(df[df['ciro_cat_rej_1t']>1].ciro_cat_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['ciro_ev_rej_1t']>1].ciro_ev_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col3.metric(label="Outros", value=f"{round(list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            col4.metric(label="Sem Religião", value=f"{round(list(df[df['ciro_non_rej_1t']>1].ciro_non_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            #col3.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_rej_1t']>1].lul_espi_rej_1t.rolling(m_m).mean())[-1],1)}%") 
            st.markdown("---")

        st.markdown(f"""
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Método utilizado para o cálculo: média móvel de {m_m} dias.</h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no resumo correspondem a última média da série temporal registrada no dia <i>{list(df.data)[-1].strftime(format='%d-%m-%Y')}</i></h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da <i>rejeição</i> dos candidatos utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)


    st.markdown("---")


    ################################################
    ## gráfico da rejeição geral - primeiro turno###
    ################################################

    with st.container():

        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #EAE6DA;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição geral:</h3><br>
        """, unsafe_allow_html=True)

        rej_vote_med_move = st.checkbox('Selecione para visualizar o gráfico da rejeição')

        if rej_vote_med_move:

            ##import image

            fig = go.Figure()
            
            ## lula
            fig.add_trace(go.Scatter(y=df.lul_ger_rej_1t, x=df.sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean(), x=df[df['lul_ger_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_rej_1t']>1].sigla)[-1], y=list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean())[-1],text=f"{int(list(df[df['lul_ger_rej_1t']>1].lul_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -0.05,
                        font=dict(size=20, color="black", family="Arial"))

            ## bolsonaro

            fig.add_trace(go.Scatter(y=df.bol_ger_rej_1t, x=df.sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_ger_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean(), x=df[df['bol_ger_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_rej_1t']>1].sigla)[-1], y=list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean())[-1],text=f"{int(list(df[df['bol_ger_rej_1t']>1].bol_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df.ciro_ger_rej_1t, x=df.sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_ger_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean(), x=df[df['ciro_ger_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_ger_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean())[-1],text=f"{int(list(df[df['ciro_ger_rej_1t']>1].ciro_ger_rej_1t.rolling(m_m15).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=110),
            title=("""
            <i>Média móvel da rejeição geral de candidatos à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            legend_title_text='<br><br>',
                            font=dict(family="arial",size=13),
                            legend=dict(
                orientation="v",
                font_family="arial",))

            fig.add_annotation(x="mar/22_pr_pesq", y=35,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_datafolha", y=35,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            fig.update_yaxes(range=[0,70])

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.07,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.88, y=1.07,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )
            st.plotly_chart(fig,use_container_width=True)

            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: <i>Método utilizado:</i> média móvel de {m_m15} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da rejeição utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 5: Mesmo com a aplicação da média móvel de 15 dias, o recorte temporal da rejeição geral de Ciro Gomes manteve-se oscilante. Trabalhamos com a hipótese de que a rejeição de Gomes associa-se à inclusão de concorrentes da 3a via como alternativas, espaço disputado por Gomes. Portanto, supomos que a variação da rejeição de Ciro Gomes seja um efeito da inclusão ou desistência de outras candiaturas.</h7><br>
            """, unsafe_allow_html=True)
        st.markdown("---")


    ###########################
    ## rejeição por religião ##
    ###########################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #EAE6DA;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição por religião:</h3><br>
        """, unsafe_allow_html=True)
        
        relig = st.selectbox('Selecione a religião:',options=['--Escolha a opção--','Católica ', 'Evangélica ', 'Espírita ', 'Sem Religião ', 'Outras Religiosidades '])

        if relig == 'Católica ':

            fig = go.Figure()
                
            ## lula

            fig.add_trace(go.Scatter(y=df.lul_cat_rej_1t, x=df.sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_cat_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_cat_rej_1t']>1].lul_cat_rej_1t.rolling(m_m).mean(), x=df[df['lul_cat_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_cat_rej_1t']>1].sigla)[-1], y=list(df[df['lul_cat_rej_1t']>1].lul_cat_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_cat_rej_1t']>1].lul_cat_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))


            ## bolsonaro

            fig.add_trace(go.Scatter(y=df.bol_cat_rej_1t, x=df.sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_cat_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_cat_rej_1t']>1].bol_cat_rej_1t.rolling(m_m).mean(), x=df[df['bol_cat_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_cat_rej_1t']>1].sigla)[-1], y=list(df[df['bol_cat_rej_1t']>1].bol_cat_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_cat_rej_1t']>1].bol_cat_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df.ciro_cat_rej_1t, x=df.sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df[df['ciro_cat_rej_1t']>1].ciro_cat_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_cat_rej_1t']>1].ciro_cat_rej_1t.rolling(m_m).mean(), x=df[df['ciro_cat_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_cat_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_cat_rej_1t']>1].ciro_cat_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_cat_rej_1t']>1].ciro_cat_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Média Móvel da rejeição de católicos por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.1,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_datafolha", y=32,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_futura", y=32,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.10,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)

             # info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: <i>Método utilizado:</i> média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da rejeição de católicos utilizamos {len(df[df['lul_cat_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)

        if relig == 'Evangélica ':
            
            fig = go.Figure()
                
            ## lula

            fig.add_trace(go.Scatter(y=df.lul_ev_rej_1t, x=df.sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ev_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ev_rej_1t']>1].lul_ev_rej_1t.rolling(m_m).mean(), x=df[df['lul_ev_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ev_rej_1t']>1].sigla)[-1], y=list(df[df['lul_ev_rej_1t']>1].lul_ev_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_ev_rej_1t']>1].lul_ev_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))


            ## bolsonaro

            fig.add_trace(go.Scatter(y=df.bol_ev_rej_1t, x=df.sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_ev_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ev_rej_1t']>1].bol_ev_rej_1t.rolling(m_m).mean(), x=df[df['bol_ev_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ev_rej_1t']>1].sigla)[-1], y=list(df[df['bol_ev_rej_1t']>1].bol_ev_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_ev_rej_1t']>1].bol_ev_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -5,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df.ciro_ev_rej_1t, x=df.sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_ev_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_ev_rej_1t']>1].ciro_ev_rej_1t.rolling(m_m).mean(), x=df[df['ciro_ev_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_ev_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_ev_rej_1t']>1].ciro_ev_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_ev_rej_1t']>1].ciro_ev_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 25,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Média Móvel da rejeição de evangélicos por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.1,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_datafolha", y=38,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_futura", y=35,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.10,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)

             # info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: <i>Método utilizado:</i> média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da rejeição de evangélicos utilizamos {len(df[df['lul_ev_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)

        if relig == 'Espírita ':
            
            fig = go.Figure()
                
            ## lula

            fig.add_trace(go.Scatter(y=df.lul_espi_rej_1t, x=df.sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_espi_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_espi_rej_1t']>1].lul_espi_rej_1t.rolling(m_m).mean(), x=df[df['lul_espi_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_espi_rej_1t']>1].sigla)[-1], y=list(df[df['lul_espi_rej_1t']>1].lul_espi_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_espi_rej_1t']>1].lul_espi_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))


            ## bolsonaro

            fig.add_trace(go.Scatter(y=df.bol_espi_rej_1t, x=df.sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_espi_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_espi_rej_1t']>1].bol_espi_rej_1t.rolling(m_m).mean(), x=df[df['bol_espi_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_espi_rej_1t']>1].sigla)[-1], y=list(df[df['bol_espi_rej_1t']>1].bol_espi_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_espi_rej_1t']>1].bol_espi_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df.ciro_espi_rej_1t, x=df.sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_espi_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_espi_rej_1t']>1].ciro_espi_rej_1t.rolling(m_m).mean(), x=df[df['ciro_espi_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_espi_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_espi_rej_1t']>1].ciro_espi_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_espi_rej_1t']>1].ciro_espi_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Média Móvel da rejeição de espíritas por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.1,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_datafolha", y=30,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_futura", y=25,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.10,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)
            
             # info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: <i>Método utilizado:</i> média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da rejeição de espíritas utilizamos {len(df[df['lul_espi_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)

        if relig == 'Outras Religiosidades ':
            
            fig = go.Figure()
                
            ## lula

            fig.add_trace(go.Scatter(y=df.lul_out_rej_1t, x=df.sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_out_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean(), x=df[df['lul_out_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_out_rej_1t']>1].sigla)[-1], y=list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_out_rej_1t']>1].lul_out_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))


            ## bolsonaro

            fig.add_trace(go.Scatter(y=df.bol_out_rej_1t, x=df.sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_out_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean(), x=df[df['bol_out_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_out_rej_1t']>1].sigla)[-1], y=list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_out_rej_1t']>1].bol_out_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df.ciro_out_rej_1t, x=df.sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_out_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean(), x=df[df['ciro_out_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_out_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_out_rej_1t']>1].ciro_out_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Média Móvel da rejeição de outras religiões por candidato à presidência (1º turno)<i><br>
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

            fig.add_annotation(x="mar/22_datafolha", y=30,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_futura", y=25,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.10,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)

             # info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Método utilizado: média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da rejeição de outras religiões utilizamos {len(df[df['lul_out_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)
            
        if relig == 'Sem Religião ':
            
            fig = go.Figure()
                    
            ## lula

            fig.add_trace(go.Scatter(y=df.lul_non_rej_1t, x=df.sigla, mode='markers', name='Rejeição Lula',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_non_rej_1t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_non_rej_1t']>1].lul_non_rej_1t.rolling(m_m).mean(), x=df[df['lul_non_rej_1t']>1].sigla, mode='lines', name='Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_non_rej_1t']>1].sigla)[-1], y=list(df[df['lul_non_rej_1t']>1].lul_non_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['lul_non_rej_1t']>1].lul_non_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))


            ## bolsonaro

            fig.add_trace(go.Scatter(y=df.bol_non_rej_1t, x=df.sigla, mode='markers', name='Rejeição Bolsonaro',
                                    marker=dict(
                                    size=5,
                                    color=df.bol_non_rej_1t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_non_rej_1t']>1].bol_non_rej_1t.rolling(m_m).mean(), x=df[df['bol_non_rej_1t']>1].sigla,mode='lines', name='Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_non_rej_1t']>1].sigla)[-1], y=list(df[df['bol_non_rej_1t']>1].bol_non_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['bol_non_rej_1t']>1].bol_non_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## ciro gomes

            fig.add_trace(go.Scatter(y=df.ciro_non_rej_1t, x=df.sigla, mode='markers', name='Rejeição Ciro',
                                    marker=dict(
                                    size=5,
                                    color=df.ciro_non_rej_1t, #set color equal to a variable
                                    colorscale='Greens')))

            fig.add_trace(go.Scatter(y=df[df['ciro_non_rej_1t']>1].ciro_non_rej_1t.rolling(m_m).mean(), x=df[df['ciro_non_rej_1t']>1].sigla,mode='lines', name='Ciro',
                                    line=dict(color='seagreen', width=2.5)))

            fig.add_annotation(x=list(df[df['ciro_non_rej_1t']>1].sigla)[-1], y=list(df[df['ciro_non_rej_1t']>1].ciro_non_rej_1t.rolling(m_m).mean())[-1],text=f"{int(list(df[df['ciro_non_rej_1t']>1].ciro_non_rej_1t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## detalhes

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            title=("""
            <i>Média Móvel da rejeição dos sem religião por candidato à presidência (1º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Rejeição (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.1,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial",))

            fig.add_annotation(x="mar/22_datafolha", y=35,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_futura", y=29,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.10,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            st.plotly_chart(fig,use_container_width=True)
            # info
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Método utilizado: média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df[df['lul_ger_rej_1t']>1].data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 4: Para o cálculo da rejeição dos sem religião utilizamos {len(df[df['lul_non_rej_1t']>1])} pesquisas eleitorais.</h7><br>
            """, unsafe_allow_html=True)
    
    st.markdown("---")


########################################################
## rejeição por religião e candidato segundo instituto##
########################################################

    institutos2 = list(set(df['nome_instituto']))
    institutos2.insert(0, ' --Escolha o instituto-- ')

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #EAE6DA;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Rejeição por religião e candidato segundo instituto de pesquisa: </h3><br>
        """, unsafe_allow_html=True)

        col, col1 = st.columns(2)
        with col:
            inst = st.selectbox('Selecione o instituto de pesquisa:',options=institutos2)
        with col1:
            ##dados retirados 'Espírita', 'Umbanda/Candomblé', 'Ateu',
            rel = st.selectbox('Escolha a religião:',options=[' --Escolha a religião-- ',' Católica ', ' Evangélica ', ' Outras Religiosidades ', ' Sem Religião '])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            if rel == ' Católica ':
                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'cat_rej'
                rel = 'católicos'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)

            if rel == ' Evangélica ':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'ev_rej'
                rel = 'evangélicos'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)

            if rel == ' Espírita ':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'espi_rej'
                rel = 'espíritas'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            if rel == ' Sem Religião ':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'non_rej'
                rel = 'sem religião'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            if rel == ' Outras Religiosidades ':

                fonte = df.query(f"nome_instituto =='{inst}'")
                religi_escolhida = 'out_rej'
                rel = 'outras religiões'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                ##ciro gomes
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
                                        line=dict(color='green', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
                                        line=dict(color='green', width=1, dash='dot')))

                fig.update_layout(width = 800, height = 800, template = 'plotly', margin=dict(r=70, l=80, b=4, t=160),
                        title=(f"""
                        Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.13,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,60])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=1.05, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=1.05, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            
            # if rel == ' Umbanda/Candomblé ':

            #     fonte = df.query(f"nome_instituto =='{inst}'")
            #     religi_escolhida = 'umb_can_rej'
            #     rel = 'umbanda e candomblé'

            #     fig = go.Figure()
            #     ##lula
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
            #                             line=dict(color='firebrick', width=2.5),legendrank=1))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
            #                             line=dict(color='firebrick', width=1, dash='dot')))
            #     ##bolsonaro
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
            #                             line=dict(color='royalblue', width=2.5),legendrank=2))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
            #                             line=dict(color='royalblue', width=1, dash='dot')))
            #     ##ciro gomes
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
            #                             line=dict(color='green', width=2.5),legendrank=3))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
            #                             line=dict(color='green', width=1, dash='dot')))

            #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            #             title=(f"""
            #             Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
            #             <br>
            #             <br>
            #             """),
            #                             xaxis_title='Mês, ano e instituto de pesquisa',
            #                             yaxis_title='Intenção de voto (%)',
            #                             font=dict(family="arial",size=13),
            #                             legend=dict(
            #                 yanchor="auto",
            #                 y=1.15,
            #                 xanchor="auto",
            #                 x=0.4,
            #                 orientation="h",
            #                 font_family="arial",))
            #     fig.update_xaxes(tickangle = 300,title_font_family="arial")
            #     fig.update_yaxes(range=[0,90])

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
            #             xref="paper", yref="paper",
            #             x=.99, y=1.03,
            #             sizex=0.1, sizey=0.1,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source=agre,
            #             xref="paper", yref="paper",
            #             x=.99, y=1.08,
            #             sizex=0.12, sizey=0.12,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )
                
            #     st.plotly_chart(fig,use_container_width=True)
            

            # if rel == ' Ateu ':

            #     fonte = df.query(f"nome_instituto =='{inst}'")
            #     religi_escolhida = 'ateu_rej'
            #     rel = 'ateus'

            #     fig = go.Figure()
            #     ##lula
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_1t'], mode='lines+markers', name=f"Lula - {rel}",
            #                             line=dict(color='firebrick', width=2.5),legendrank=1))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_1t'],mode='lines+markers', name=f"Lula - geral", 
            #                             line=dict(color='firebrick', width=1, dash='dot')))
            #     ##bolsonaro
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_1t'], mode='lines+markers', name=f"Bolsonaro - {rel}",
            #                             line=dict(color='royalblue', width=2.5),legendrank=2))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_1t'],mode='lines+markers', name=f"Bolsonaro - geral", 
            #                             line=dict(color='royalblue', width=1, dash='dot')))
            #     ##ciro gomes
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'ciro_{religi_escolhida}_1t'], mode='lines+markers', name=f"Ciro Gomes - {rel}",
            #                             line=dict(color='green', width=2.5),legendrank=3))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['ciro_ger_1t'],mode='lines+markers', name=f"Ciro Gomes - geral", 
            #                             line=dict(color='green', width=1, dash='dot')))

            #     fig.update_layout(width = 810, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            #             title=(f"""
            #             Rejeição 'geral' e de '{rel}' por candidato segundo '{inst.title()}' (1º turno)
            #             <br>
            #             <br>
            #             """),
            #                             xaxis_title='Mês, ano e instituto de pesquisa',
            #                             yaxis_title='Intenção de voto (%)',
            #                             font=dict(family="arial",size=13),
            #                             legend=dict(
            #                 yanchor="auto",
            #                 y=1.15,
            #                 xanchor="auto",
            #                 x=0.4,
            #                 orientation="h",
            #                 font_family="arial",))
            #     fig.update_xaxes(tickangle = 300,title_font_family="arial")
            #     fig.update_yaxes(range=[-0.5,95])

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
            #             xref="paper", yref="paper",
            #             x=1.05, y=1.03,
            #             sizex=0.1, sizey=0.1,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source=agre,
            #             xref="paper", yref="paper",
            #             x=1.05, y=1.08,
            #             sizex=0.12, sizey=0.12,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )
                
            #     st.plotly_chart(fig,use_container_width=True)
                

        st.markdown(f"""
        <h7 style='text-align: center; color:#606060;font-family:arial'>Nota 1: O percentual da <i>rejeição</i> dos candidatos foi obtida pela resposta de eleitores que declaram "não votar de jeito nenhum” em determinado incumbente.</h7><br>
        <h7 style='text-align: center; color:#606060;font-family:arial'>Nota 12 Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte religioso.</h7>
        """, unsafe_allow_html=True)
    st.markdown("---")

#################################################
##avaliação ruim e péssima do governo bolsonaro##   FICARÁ BLOQUEADO ATÉ O INÍCIO DAS ELEIÇÕES.
#################################################

    # st.markdown(f"""
    #     <h3 style='text-align: center; color: #303030; font-family:segoe UI; text-rendering: optimizelegibility;background-color: #FFD662;'>3. Avaliação do governo Bolsonaro</h3>
    #     """, unsafe_allow_html=True)
    # st.markdown("---")

    # ####################
    # ##resumo avaliação##
    # ####################

    # with st.container():
    #     st.markdown(f"""
    #     <br>
    #     <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #EDF1FF;'>Resumo - avaliação ruim e péssima geral e por religião: </h3><br>
    #     <br>
    #     """, unsafe_allow_html=True)


    #     adm_bolsonaro = st.checkbox(' Selecione para visualizar os dados da avalização do governo Bolsonaro.')

    #     if adm_bolsonaro:

    #         ## coluna 1
    #         bol = Image.open('bolso_image.jpeg')
    #         col0,col, col1, col2, col3, col4 = st.columns(6)
    #         col0.image(bol,width=100)
    #         col.metric(label="Geral", value=f"{round(list(df[df['ava_gov_bol_GERAL']>1].ava_gov_bol_GERAL.rolling(m_m).mean())[-1],1)}%") 
    #         col1.metric(label="Católicos", value=f"{round(list(df[df['ava_gov_bol_cat']>1].ava_gov_bol_cat.rolling(m_m).mean())[-1],1)}%") 
    #         col2.metric(label="Evangélicos", value=f"{round(list(df[df['ava_gov_bol_ev']>1].ava_gov_bol_ev.rolling(m_m).mean())[-1],1)}%") 
    #         col3.metric(label="Outros", value=f"{round(list(df[df['ava_gov_bol_out']>1].ava_gov_bol_out.rolling(m_m).mean())[-1],1)}%") 
    #         col4.metric(label="Sem Religião", value=f"{round(list(df[df['ava_gov_bol_non']>1].ava_gov_bol_non.rolling(m_m).mean())[-1],1)}%")
    #         #col3.metric(label="Espíritas", value=f"{round(list(df[df['ava_gov_bol_espi']>1].ava_gov_bol_espi.rolling(m_m).mean())[-1],1)}%") 
    #         st.markdown(f"""
    #         <br>
    #         <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado para o cálculo: média móvel de {m_m} dias.</h7><br>
    #         <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no resumo correspondem a última média da série temporal registrada no dia <i>{list(df[df['ava_gov_bol_GERAL']>1].data)[-1].strftime(format='%d-%m-%Y')}</i></h7><br>
    #         <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Para a produção dos dados da <i>aprovação</i> do governo bolsonaro utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais. Destacamos a reprovação por segmento religioso através da soma dos percentuais das respostas 'ruim e péssimo'.</h7><br>
    #         <br>
    #         """, unsafe_allow_html=True)
    #     st.markdown("---")

############################
###Avaliação por religião###
############################

    # with st.container():
    #     st.markdown(f"""
    #     <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #EDF1FF;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
    #     <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
    #     </svg> Avaliação ruim e péssima por religião:</h3><br>
    #     """, unsafe_allow_html=True)

    #     aval_vote_med_move = st.checkbox('Selecione para visualizar o gráfico da avaliação do governo Bolsonaro')

    #     if aval_vote_med_move:

    #         fig = go.Figure()

    #         ## católicos

    #         fig.add_trace(go.Scatter(y=df.ava_gov_bol_cat, x=df.sigla, mode='markers', name='aval_cat',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df.ava_gov_bol_cat, #set color equal to a variable
    #                                 colorscale='peach')))

    #         fig.add_trace(go.Scatter(y=df[df['ava_gov_bol_cat']>1].ava_gov_bol_cat.rolling(m_m).mean(), x=df[df['ava_gov_bol_cat']>1].sigla, mode='lines', name='católicos',
    #                                 line=dict(color='#802b00', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ava_gov_bol_cat']>1].sigla)[-1], y=list(df[df['ava_gov_bol_cat']>1].ava_gov_bol_cat.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['ava_gov_bol_cat']>1].ava_gov_bol_cat.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))


    #         ## evangélicos

    #         fig.add_trace(go.Scatter(y=df.ava_gov_bol_ev, x=df.sigla, mode='markers', name='aval_ev',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df.ava_gov_bol_ev, #set color equal to a variable
    #                                 colorscale='tropic')))

    #         fig.add_trace(go.Scatter(y=df[df['ava_gov_bol_ev']>1].ava_gov_bol_ev.rolling(m_m).mean(), x=df[df['ava_gov_bol_ev']>1].sigla,mode='lines', name='evangélicos',
    #                                 line=dict(color='#80ccff', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ava_gov_bol_ev']>1].sigla)[-1], y=list(df[df['ava_gov_bol_ev']>1].ava_gov_bol_ev.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['ava_gov_bol_ev']>1].ava_gov_bol_ev.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))

    #         ## outras religiões

    #         fig.add_trace(go.Scatter(y=df.ava_gov_bol_out, x=df.sigla, mode='markers', name='aval_out',
    #                                 marker=dict(
    #                                 size=5,
    #                                 color=df.ava_gov_bol_out, #set color equal to a variable
    #                                 colorscale='Greens')))

    #         fig.add_trace(go.Scatter(y=df[df['ava_gov_bol_out']>1].ava_gov_bol_out.rolling(m_m).mean(), x=df[df['ava_gov_bol_out']>1].sigla,mode='lines', name='outras religiões',
    #                                 line=dict(color='#808080', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ava_gov_bol_out']>1].sigla)[-1], y=list(df[df['ava_gov_bol_out']>1].ava_gov_bol_out.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['ava_gov_bol_out']>1].ava_gov_bol_out.rolling(m_m).mean())[-1])}%",
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     ax = 40, ay = 0,
    #                     font=dict(size=20, color="black", family="Arial"))


    #         ## sem religião 

    #         fig.add_trace(go.Scatter(y=df.ava_gov_bol_non, x=df.sigla, mode='markers', name='aval_sem_religião',
    #                                  marker=dict(
    #                                  size=5,
    #                                  color=df.ava_gov_bol_non, #set color equal to a variable
    #                                  colorscale='Greens')))

    #         fig.add_trace(go.Scatter(y=df[df['ava_gov_bol_non']>1].ava_gov_bol_non.rolling(m_m).mean(), x=df[df['ava_gov_bol_non']>1].sigla,mode='lines', name='aval_sem_religião',
    #                                  line=dict(color='seagreen', width=2.5)))

    #         fig.add_annotation(x=list(df[df['ava_gov_bol_non']>1].sigla)[-1], y=list(df[df['ava_gov_bol_non']>1].ava_gov_bol_non.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['ava_gov_bol_non']>1].ava_gov_bol_non.rolling(m_m).mean())[-1])}%",
    #                      showarrow=True,
    #                      arrowhead=1,
    #                      ax = 40, ay = 0,
    #                      font=dict(size=20, color="black", family="Arial"))

    #         ## detalhes

    #         fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
    #         title=("""
    #         <i>Avaliação negativa de Bolsonaro por religião (1º turno)<i><br>
    #         """),
    #                         xaxis_title='Mês, ano e instituto de pesquisa',
    #                         yaxis_title='Rejeição (%)',
    #                         font=dict(family="arial",size=13),
    #                         legend=dict(
    #             yanchor="auto",
    #             y=1.1,
    #             xanchor="auto",
    #             x=0.5,
    #             orientation="h",
    #             font_family="arial",))

    #         fig.add_annotation(x="mar/22_fsb", y=35,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
    #         fig.add_annotation(x="mai/22_fsb", y=32,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

    #         fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

    #         # Add image
    #         fig.add_layout_image(
    #             dict(
    #                 source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
    #                 xref="paper", yref="paper",
    #                 x=.99, y=1.12,
    #                 sizex=0.1, sizey=0.1,
    #                 xanchor="right", yanchor="bottom"
    #             )
    #         )

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

    #         st.plotly_chart(fig,use_container_width=True)

            
    #         ## info
    #     st.markdown(f"""
    #     <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado para o cálculo: média móvel de {m_m} dias.</h7><br>
    #     <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Para a produção dos gráficos sobre a <i>aprovação</i> do governo bolsonaro utilizamos {len(df[df['lul_ger_rej_1t']>1])} pesquisas eleitorais. Destacamos a reprovação por segmento religioso através do registro das respostas 'ruim e péssimo'.</h7><br>
    #     """, unsafe_allow_html=True)
    #     st.markdown("---")


#############################################################################################################################
                                                        ### segundo turno ######
#############################################################################################################################

if options_turn == 'Segundo Turno':

    st.markdown(f"""
        <h2 style='text-align: center; color: #303030; font-family:tahoma; text-rendering: optimizelegibility'>Segundo Turno</h2>
        <br>
        """, unsafe_allow_html=True)
    st.markdown("---")


##################
##resumo#########
#################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'>Resumo - intenção de voto por candidato</h3> \n
        <br>""", unsafe_allow_html=True)

        int_vot_lula = st.checkbox('Lula ')

        if int_vot_lula:
            ## coluna 1
            lul = Image.open('lula_perfil.jpg')
            col0, col, col1, col2, col3, col4, col5 = st.columns(7)
            col0.image(lul,width=105,channels="B")
            col.metric(label="Geral", value=f"{round(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Católicos", value=f"{round(list(df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1],1),1)}")
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1],1),1)}")
            col3.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1],1)-round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1),1)}")
            col4.metric(label="Outros", value=f"{round(list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1),1)}")
            col5.metric(label="Sem Religião", value=f"{round(list(df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1],1),1)}")
            ## coluna 2
            #col4, col5, col6, col7, col8 = st.columns(5)
            #col4.metric(label="",value="")
            # col5.metric(label="Umbanda/Candomblé", value=f"{round(list(df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1],1),1)}")
            # col6.metric(label="Ateu", value=f"{round(list(df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1],1),1)}")
            # col3.metric(label="Espíritas", value=f"{round(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1],1)-round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1),1)}")
            # ## info
            # st.caption('* Dados na cor verde indicam a vantagem de Lula em relação a Bolsonaro, e vermelho, desvantagem.')
            st.markdown("---")

        int_vot_bolsonaro = st.checkbox('Bolsonaro ')

        if int_vot_bolsonaro:
            ## coluna 1
            bol = Image.open('bolso_image.jpeg')
            col0, col, col1, col2, col3, col4, col5 = st.columns(7)
            col0.image(bol,width=100)
            col.metric(label="Geral", value=f"{round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1],1),1)}%")
            col1.metric(label="Católicos", value=f"{round(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean())[-1],1),1)}")
            col2.metric(label="Evangélicos", value=f"{round(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean())[-1],1),1)}")
            col3.metric(label="Espíritas", value=f"{round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1],1)-round(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1],1),1)}")
            col4.metric(label="Outros", value=f"{round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1],1),1)}")
            col5.metric(label="Sem Religião", value=f"{round(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1],1)}%") #, delta=f"{round(round(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean())[-1],1),1)}")
            # ## coluna 2
            # col4, col5, col6, col7, col8 = st.columns(5)
            # col4.metric(label="",value="")
            # col5.metric(label="Umbanda/Candomblé", value=f"{round(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean())[-1],1),1)}")
            # col6.metric(label="Ateu", value=f"{round(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1],1)}%", delta=f"{round(round(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1],1) - round(list(df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean())[-1],1),1)}")
            # ## info
            # st.caption('* Dados na cor verde indicam a vantagem de Bolsonaro em relação a Lula, e vermelho, desvantagem.')
        
        st.markdown(f"""
        <br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: Método utilizado: média móvel de {m_m} dias.</h7> \n
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no resumo correspondem a última média da série temporal registrada no dia *{list(df.data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
        <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Para o cálculo do resumo da média móvel das intenções de voto geral ao segundo turno utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>
        """, unsafe_allow_html=True)
    st.markdown("---")


    ################################
    ## Média movel segundo turno###
    ################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto geral</h3>
        <br>""", unsafe_allow_html=True)

        int_vote_med_move_2t = st.checkbox('Clique para visualizar')

        if int_vote_med_move_2t:

            fig = go.Figure()
            ## lula
            fig.add_trace(go.Scatter(y=df.lul_ger_2t, x=df.sigla, mode='markers', name='Lula - geral',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_2t, #set color equal to a variable
                                    colorscale='peach')))

            fig.add_trace(go.Scatter(y=df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Int. voto Lula',
                                    line=dict(color='firebrick', width=2.5)))

            fig.add_annotation(x=list(df[df['lul_ger_2t']>1].sigla)[-1], y=list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_ger_2t']>1].lul_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                    ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Bolsonaro
            fig.add_trace(go.Scatter(y=df.bol_ger_2t, x=df.sigla, mode='markers', name='Bolsonaro - geral',
                                    marker=dict(
                                    size=5,
                                    color=df.lul_ger_2t, #set color equal to a variable
                                    colorscale='ice')))

            fig.add_trace(go.Scatter(y=df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean(), x=df[df['bol_ger_2t']>1].sigla,mode='lines', name='Int. voto Bolsonaro',
                                    line=dict(color='skyblue', width=2.5)))

            fig.add_annotation(x=list(df[df['bol_ger_2t']>1].sigla)[-1], y=list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_ger_2t']>1].bol_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                    ax = 40, ay = 0,
                        font=dict(size=20, color="black", family="Arial"))

            ## Brancos, Nulos, NS, NR 

            fig.add_trace(go.Scatter(y=df.bra_nul_ns_nr_ger_2t, x=df.sigla, mode='markers', name='Brancos, nulos, NS e NR',
                                    marker=dict(
                                    size=5,
                                    color=df.bra_nul_ns_nr_ger_2t, #set color equal to a variable
                                    colorscale='gray')))

            fig.add_trace(go.Scatter(y=df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean(), x=df[df['bra_nul_ns_nr_ger_2t']>1].sigla, mode='lines', name='Brancos, nulos, NS e NR',
                                    line=dict(color='gray', width=2.5)))

            fig.add_annotation(x=list(df[df['bra_nul_ns_nr_ger_2t']>1].sigla)[-1], y=list(df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nul_ns_nr_ger_2t']>1].bra_nul_ns_nr_ger_2t.rolling(m_m).mean())[-1])}%",
                        showarrow=True,
                        arrowhead=1,
                        ax = 40, ay = -8,
                        font=dict(size=20, color="black", family="Arial"))

            fig.update_layout(width = 1100, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=2, t=150),
            title=("""
            <i>Média móvel das intenções de voto de candidatos à presidência (2º turno)<i><br>
            """),
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=13),
                            legend=dict(
                yanchor="auto",
                y=1.12,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial"))

            fig.add_annotation(x="mar/22_poderdata_3", y=32,text="Moro<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))
            fig.add_annotation(x="mai/22_poderdata_2", y=32,text="Dória<br>desiste",showarrow=True,arrowhead=1,yanchor="bottom",ax = 0, ay = 40,font=dict(size=10, color="black", family="Arial"))

            fig.update_xaxes(tickangle = 280,rangeslider_visible=False,title_font_family="Arial")

            # Add image
            fig.add_layout_image(
                dict(
                    source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                    xref="paper", yref="paper",
                    x=.99, y=1.02,
                    sizex=0.1, sizey=0.1,
                    xanchor="right", yanchor="bottom"
                )
            )

            # Add image
            fig.add_layout_image(
                dict(
                    source=agre,
                    xref="paper", yref="paper",
                    x=.99, y=1.08,
                    sizex=0.12, sizey=0.12,
                    xanchor="right", yanchor="bottom"
                )
            )

            fig.update_yaxes(range=[0,70])

            st.plotly_chart(fig,use_container_width=True)
            st.markdown(f"""
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 1: *Método utilizado:* média móvel de {m_m} dias.</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 2: Os valores indicados no gráfico correspondem a última média da série temporal registrada no dia *{list(df.data)[-1].strftime(format='%d-%m-%Y')}*</h7><br>
            <h7 style='text-align: left; color:#606060;font-family:arial'>Nota 3: Para o cálculo da média móvel da intenção de voto geral ao segundo turno utilizamos {len(df[df['lul_ger_1t']>1])} pesquisas eleitorais.</h7><br>

            """, unsafe_allow_html=True)
    st.markdown("---")

############################
### intenção de voto média##
############################

    #########################################
    ##intenção de voto por religião 2 truno##
    #########################################

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por religião:</h3>
        <br>""", unsafe_allow_html=True)
        ## opçoes deletadas 'Espírita ', 'Umbanda/Candomblé ', 'Ateu ',
        relig2t = st.selectbox('Selecione a religião:',options=['--Escolha a opção--','Católica ', 'Evangélica ', 'Sem Religião ', 'Outras Religiosidades '])

    if relig2t == 'Católica ':

        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_cat_2t, x=df.sigla, mode='markers', name='Lula ',
                                marker=dict(
                                size=5,
                                color=df.lul_cat_2t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean(), x=df[df['bol_cat_2t']>1].sigla,mode='lines', name='Int. voto Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_cat_2t']>1].sigla)[-1], y=list(df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_cat_2t']>1].lul_cat_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_cat_2t, x=df.sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.lul_cat_2t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean(), x=df[df['bol_cat_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_cat_2t']>1].sigla)[-1], y=list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_cat_2t']>1].bol_cat_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos, Nulos 

        fig.add_trace(go.Scatter(y=df.bra_nulo_cat_2t, x=df.sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_cat_2t, #set color equal to a variable
                                colorscale='gray')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_cat_2t']>1].bra_nulo_cat_2t.rolling(m_m).mean(), x=df[df['bra_nulo_cat_2t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='gray', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_cat_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_cat_2t']>1].bra_nulo_cat_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nulo_cat_2t']>1].bra_nulo_cat_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly',margin=dict(r=80, l=80, b=2, t=150),
                            title="""
                            <i>Média móvel das intenções de voto de católicos por candidato à presidência (2º turno)<i><br>
                            """,
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=14),
                            legend=dict(
                yanchor="auto",
                y=1.12,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
        fig.update_yaxes(range=[0,70])


       # Add image
        fig.add_layout_image(
            dict(
                source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                xref="paper", yref="paper",
                x=.99, y=1.05,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.13,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )      

        st.plotly_chart(fig,use_container_width=True)

    if relig2t == 'Evangélica ':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_ev_2t, x=df.sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df.lul_ev_2t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean(), x=df[df['bol_ev_2t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_ev_2t']>1].sigla)[-1], y=list(df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_ev_2t']>1].lul_ev_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_ev_2t, x=df.sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.lul_ev_2t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean(), x=df[df['bol_ev_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_ev_2t']>1].sigla)[-1], y=list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_ev_2t']>1].bol_ev_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        
        ## Brancos, Nulos 

        fig.add_trace(go.Scatter(y=df.bra_nulo_ev_2t, x=df.sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_ev_2t, #set color equal to a variable
                                colorscale='gray')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_ev_2t']>1].bra_nulo_ev_2t.rolling(m_m).mean(), x=df[df['bra_nulo_ev_2t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='gray', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_ev_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_ev_2t']>1].bra_nulo_ev_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nulo_ev_2t']>1].bra_nulo_ev_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly',margin=dict(r=80, l=80, b=2, t=150),
                            title="""
                            <i>Média móvel das intenções de voto de evangélicos por candidato à presidência (2º turno)<i><br>
                            """,
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=14),
                            legend=dict(
                yanchor="auto",
                y=1.12,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
        fig.update_yaxes(range=[0,70])


        # Add image
        fig.add_layout_image(
            dict(
                source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                xref="paper", yref="paper",
                x=.99, y=1.05,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.13,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )      

        st.plotly_chart(fig,use_container_width=True)

    if relig2t == 'Sem Religião ':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_non_2t, x=df.sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df.lul_non_2t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean(), x=df[df['bol_non_2t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_non_2t']>1].sigla)[-1], y=list(df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_non_2t']>1].lul_non_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_non_2t, x=df.sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.lul_non_2t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean(), x=df[df['bol_non_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_non_2t']>1].sigla)[-1], y=list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_non_2t']>1].bol_non_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Brancos, Nulos 

        fig.add_trace(go.Scatter(y=df.bra_nulo_non_2t, x=df.sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_non_2t, #set color equal to a variable
                                colorscale='gray')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_non_2t']>1].bra_nulo_non_2t.rolling(m_m).mean(), x=df[df['bra_nulo_non_2t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='gray', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_non_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_non_2t']>1].bra_nulo_non_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nulo_non_2t']>1].bra_nulo_non_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly',margin=dict(r=80, l=80, b=2, t=150),
                            title="""
                            <i>Média móvel das intenções de voto dos sem religião por candidato à presidência (2º turno)<i><br>
                            """,
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=14),
                            legend=dict(
                yanchor="auto",
                y=1.13,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
        fig.update_yaxes(range=[0,70])


        # Add image
        fig.add_layout_image(
            dict(
                source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                xref="paper", yref="paper",
                x=.99, y=1.05,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.13,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )      

        st.plotly_chart(fig,use_container_width=True)

    if relig2t == 'Outras Religiosidades ':
        fig = go.Figure()
        ## lula
        fig.add_trace(go.Scatter(y=df.lul_out_2t, x=df.sigla, mode='markers', name='Int. voto Lula',
                                marker=dict(
                                size=5,
                                color=df.lul_out_2t, #set color equal to a variable
                                colorscale='peach')))

        fig.add_trace(go.Scatter(y=df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean(), x=df[df['bol_out_2t']>1].sigla,mode='lines', name='Lula',
                                line=dict(color='firebrick', width=2.5)))

        fig.add_annotation(x=list(df[df['lul_out_2t']>1].sigla)[-1], y=list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_out_2t']>1].lul_out_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))

        ## Bolsonaro
        fig.add_trace(go.Scatter(y=df.bol_out_2t, x=df.sigla, mode='markers', name='Int. voto Bolsonaro',
                                marker=dict(
                                size=5,
                                color=df.lul_out_2t, #set color equal to a variable
                                colorscale='ice')))

        fig.add_trace(go.Scatter(y=df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean(), x=df[df['bol_out_2t']>1].sigla,mode='lines', name='Bolsonaro',
                                line=dict(color='skyblue', width=2.5)))

        fig.add_annotation(x=list(df[df['bol_out_2t']>1].sigla)[-1], y=list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_out_2t']>1].bol_out_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = 0,
                    font=dict(size=20, color="black", family="Arial"))
        
        ## Brancos, Nulos 

        fig.add_trace(go.Scatter(y=df.bra_nulo_out_2t, x=df.sigla, mode='markers', name='Brancos e nulos',
                                marker=dict(
                                size=5,
                                color=df.bra_nulo_out_2t, #set color equal to a variable
                                colorscale='gray')))

        fig.add_trace(go.Scatter(y=df[df['bra_nulo_out_2t']>1].bra_nulo_out_2t.rolling(m_m).mean(), x=df[df['bra_nulo_out_2t']>1].sigla, mode='lines', name='Brancos e nulos',
                                line=dict(color='gray', width=2.5)))

        fig.add_annotation(x=list(df[df['bra_nulo_out_2t']>1].sigla)[-1], y=list(df[df['bra_nulo_out_2t']>1].bra_nulo_out_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bra_nulo_out_2t']>1].bra_nulo_out_2t.rolling(m_m).mean())[-1])}%",
                    showarrow=True,
                    arrowhead=1,
                    ax = 40, ay = -8,
                    font=dict(size=20, color="black", family="Arial"))

        fig.update_layout(width = 1100, height = 800, template = 'plotly',margin=dict(r=80, l=80, b=2, t=150),
                            title="""
                            <i>Média móvel das intenções de voto de católicos por candidato à presidência (2º turno)<i><br>
                            """,
                            xaxis_title='Mês, ano e instituto de pesquisa',
                            yaxis_title='Intenção de voto (%)',
                            font=dict(family="arial",size=14),
                            legend=dict(
                yanchor="auto",
                y=1.13,
                xanchor="auto",
                x=0.4,
                orientation="h",
                font_family="arial"))

        fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
        fig.update_yaxes(range=[0,70])


        # Add image
        fig.add_layout_image(
            dict(
                source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                xref="paper", yref="paper",
                x=.99, y=1.05,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )

        # Add image
        fig.add_layout_image(
            dict(
                source=agre,
                xref="paper", yref="paper",
                x=.99, y=1.13,
                sizex=0.12, sizey=0.12,
                xanchor="right", yanchor="bottom"
            )
        )      

        st.plotly_chart(fig,use_container_width=True)

        # if relig2t == 'Espírita ':
    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_espi_2t']>1].lul_espi_2t, x=df[df['lul_espi_2t']>1].data, mode='markers', name='int_vot_espi_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_espi_2t']>1].lul_espi_2t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean(), x=df[df['bol_espi_2t']>1].data,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_espi_2t']>1].data)[-1], y=list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_espi_2t']>1].lul_espi_2t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                   #  ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_espi_2t']>1].bol_espi_2t, x=df[df['bol_espi_2t']>1].data, mode='markers', name='int_vot_espi_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_espi_2t']>1].lul_espi_2t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean(), x=df[df['bol_espi_2t']>1].data,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_espi_2t']>1].data)[-1], y=list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_espi_2t']>1].bol_espi_2t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'none',
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     legend=dict(
    #         yanchor="auto",
    #         y=1.1,
    #         xanchor="auto",
    #         x=0.5,
    #         orientation="h"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=False)

    #     st.plotly_chart(fig,use_container_width=True)

    # if relig2t == 'Umbanda/Candomblé ':

    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_umb_can_2t']>1].lul_umb_can_2t, x=df[df['lul_umb_can_2t']>1].data, mode='markers', name='int_vot_umb_can_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_umb_can_2t']>1].lul_umb_can_2t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean(), x=df[df['bol_umb_can_2t']>1].data,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_umb_can_2t']>1].data)[-1], y=list(df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_umb_can_2t']>1].lul_umb_can_2t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                   #  ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_umb_can_2t']>1].bol_umb_can_2t, x=df[df['bol_umb_can_2t']>1].data, mode='markers', name='int_vot_umb_can_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_umb_can_2t']>1].lul_umb_can_2t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean(), x=df[df['bol_umb_can_2t']>1].data,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_umb_can_2t']>1].data)[-1], y=list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_umb_can_2t']>1].bol_umb_can_2t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'none',
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     legend=dict(
    #         yanchor="auto",
    #         y=1.1,
    #         xanchor="auto",
    #         x=0.5,
    #         orientation="h"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
    #     st.plotly_chart(fig,use_container_width=True)

    # if relig2t == 'Ateu ':
    #     fig = go.Figure()
    #     ## lula
    #     fig.add_trace(go.Scatter(y=df[df['lul_ateu_2t']>1].lul_ateu_2t, x=df[df['lul_ateu_2t']>1].data, mode='markers', name='int_vot_ateu_lula',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['lul_ateu_2t']>1].lul_ateu_2t, #set color equal to a variable
    #                             colorscale='peach')))

    #     fig.add_trace(go.Scatter(y=df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean(), x=df[df['bol_ateu_2t']>1].data,mode='lines', name='Lula',
    #                             line=dict(color='firebrick', width=2.5)))

    #     fig.add_annotation(x=list(df[df['lul_ateu_2t']>1].data)[-1], y=list(df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['lul_ateu_2t']>1].lul_ateu_2t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                    # ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     ## Bolsonaro
    #     fig.add_trace(go.Scatter(y=df[df['bol_ateu_2t']>1].bol_ateu_2t, x=df[df['bol_ateu_2t']>1].data, mode='markers', name='int_vot_ateu_bolsonaro',
    #                             marker=dict(
    #                             size=5,
    #                             color=df[df['bol_ateu_2t']>1].lul_ateu_2t, #set color equal to a variable
    #                             colorscale='ice')))

    #     fig.add_trace(go.Scatter(y=df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean(), x=df[df['bol_ateu_2t']>1].data,mode='lines', name='Bolsonaro',
    #                             line=dict(color='skyblue', width=2.5)))

    #     fig.add_annotation(x=list(df[df['bol_ateu_2t']>1].data)[-1], y=list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1] ,text=f"{int(list(df[df['bol_ateu_2t']>1].bol_ateu_2t.rolling(m_m).mean())[-1])}%",
    #                 showarrow=True,
    #                 arrowhead=1,
                   #  ax = 40, ay = 0,
    #                 font=dict(size=20, color="black", family="Arial"))

    #     fig.update_layout(width = 1000, height = 800, template = 'none',
    #                     xaxis_title='Mês, ano e instituto de pesquisa',
    #                     yaxis_title='Intenção de voto (%)',
    #                     legend=dict(
    #         yanchor="auto",
    #         y=1.1,
    #         xanchor="auto",
    #         x=0.5,
    #         orientation="h"))

    #     fig.update_xaxes(tickangle = 280,rangeslider_visible=False)
    #     st.plotly_chart(fig,use_container_width=True)

        st.caption('**Obs.:** Em alguns casos, a combinção de dados retornará um gráfico em branco. \n Isso indica que instituto de pesquisa selecionado não coletou dados da categoria.')

    st.markdown(f"""
    <h7 style='text-align: left; color:#606060;font-family:arial'>1) *Método utilizado:* média móvel de {m_m} dias.</h7>
    """, unsafe_allow_html=True)
    st.markdown("---")


    #####################################
    ### dados por instituto de pesquisa##
    #####################################

    institutos = list(set(df['nome_instituto']))
    institutos.insert(0, '--Escolha a opção--')

    with st.container():
        st.markdown(f"""
        <h3 style='text-align: left; color: #303030; font-family:Segoe UI; text-rendering: optimizelegibility; background-color: #e6e6e6;'><svg xmlns="http://www.w3.org/2000/svg" width="30" height="26" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 18">
        <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg> Intenção de voto por instituto de pesquisa e religião:</h3> \n
        <br>""", unsafe_allow_html=True)

        col, col1 = st.columns(2)
        with col:
            inst2 = st.selectbox('Selecione o instituto de pesquisa:',options=institutos)
        with col1:
            ##dado retirado 'Espírita', 'Umbanda/Candomblé', 'Ateu',
            rel2 = st.selectbox('Escolha a religião:',options=['--Escolha a opção--','Católica', 'Evangélica', 'Sem Religião', 'Outras Religiosidades'])

        col1, col2, col3 = st.columns([.5,3,.5])

        with col2:
            if rel2 == 'Católica':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                religi_escolhida = 'cat'
                rel2 = 'católicos'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                
                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)


            if rel2== 'Evangélica':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                religi_escolhida = 'ev'
                rel2= 'evangélicos'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                
                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)


            if rel2== 'Espírita':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                religi_escolhida = 'espi'
                rel2= 'espíritas'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                
                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            

            if rel2== 'Sem Religião':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                religi_escolhida = 'non'
                rel2= 'sem religião'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot')))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
                                        line=dict(color='royalblue', width=2.5),legendrank=2))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot')))
                
                fig.update_layout(width = 800, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.15,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,70])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=.99, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=.99, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            

            if rel2== 'Outras Religiosidades':

                fonte = df.query(f"nome_instituto =='{inst2}'")
                religi_escolhida = 'out'
                rel2= 'outras religiões'

                fig = go.Figure()
                ##lula
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
                                        line=dict(color='firebrick', width=2.5),legendrank=1))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
                                        line=dict(color='firebrick', width=1, dash='dot'),legendrank=2))
                ##bolsonaro
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
                                        line=dict(color='royalblue', width=2.5),legendrank=3))
                fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
                                        line=dict(color='royalblue', width=1, dash='dot'),legendrank=4))
                
                fig.update_layout(width = 800, height = 800, template = 'plotly', margin=dict(r=70, l=80, b=4, t=160),
                        title=(f"""
                        Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
                        <br>
                        <br>
                        """),
                                        xaxis_title='Mês, ano e instituto de pesquisa',
                                        yaxis_title='Intenção de voto (%)',
                                        font=dict(family="arial",size=13),
                                        legend=dict(
                            yanchor="auto",
                            y=1.13,
                            xanchor="auto",
                            x=0.4,
                            orientation="h",
                            font_family="arial",))
                fig.update_xaxes(tickangle = 300,title_font_family="arial")
                fig.update_yaxes(range=[0,60])

                # Add image
                fig.add_layout_image(
                    dict(
                        source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
                        xref="paper", yref="paper",
                        x=1.05, y=1.03,
                        sizex=0.1, sizey=0.1,
                        xanchor="right", yanchor="bottom"
                    )
                )

                # Add image
                fig.add_layout_image(
                    dict(
                        source=agre,
                        xref="paper", yref="paper",
                        x=1.05, y=1.08,
                        sizex=0.12, sizey=0.12,
                        xanchor="right", yanchor="bottom"
                    )
                )
                
                st.plotly_chart(fig,use_container_width=True)
            
            
            # if rel2== 'Umbanda/Candomblé':

            #     fonte = df.query(f"nome_instituto =='{inst2}'")
            #     religi_escolhida = 'umb_can'
            #     rel2= 'umbanda e candomblé'

            #     fig = go.Figure()
            #     ##lula
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
            #                             line=dict(color='firebrick', width=2.5),legendrank=1))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
            #                             line=dict(color='firebrick', width=1, dash='dot')))
            #     ##bolsonaro
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
            #                             line=dict(color='royalblue', width=2.5),legendrank=2))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
            #                             line=dict(color='royalblue', width=1, dash='dot')))
            #
            #     fig.update_layout(width = 1000, height = 800, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            #             title=(f"""
            #             Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
            #             <br>
            #             <br>
            #             """),
            #                             xaxis_title='Mês, ano e instituto de pesquisa',
            #                             yaxis_title='Intenção de voto (%)',
            #                             font=dict(family="arial",size=13),
            #                             legend=dict(
            #                 yanchor="auto",
            #                 y=1.15,
            #                 xanchor="auto",
            #                 x=0.4,
            #                 orientation="h",
            #                 font_family="arial",))
            #     fig.update_xaxes(tickangle = 300,title_font_family="arial")
            #     fig.update_yaxes(range=[0,90])

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
            #             xref="paper", yref="paper",
            #             x=.99, y=1.03,
            #             sizex=0.1, sizey=0.1,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source=agre,
            #             xref="paper", yref="paper",
            #             x=.99, y=1.08,
            #             sizex=0.12, sizey=0.12,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )
                
            #     st.plotly_chart(fig,use_container_width=True)
            

            # if rel2== 'Ateu':

            #     fonte = df.query(f"nome_instituto =='{inst2}'")
            #     religi_escolhida = 'ateu'
            #     rel2= 'ateus'

            #     fig = go.Figure()
            #     ##lula
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'lul_{religi_escolhida}_2t'], mode='lines+markers', name=f"Lula - {rel2}",
            #                             line=dict(color='firebrick', width=2.5),legendrank=1))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['lul_ger_2t'],mode='lines+markers', name=f"Lula - geral", 
            #                             line=dict(color='firebrick', width=1, dash='dot')))
            #     ##bolsonaro
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte[f'bol_{religi_escolhida}_2t'], mode='lines+markers', name=f"Bolsonaro - {rel2}",
            #                             line=dict(color='royalblue', width=2.5),legendrank=2))
            #     fig.add_trace(go.Scatter(x=fonte['sigla'], y=fonte['bol_ger_2t'],mode='lines+markers', name=f"Bolsonaro - geral", 
            #                             line=dict(color='royalblue', width=1, dash='dot')))

            #     fig.update_layout(width = 810, height = 700, template = 'plotly', margin=dict(r=80, l=80, b=4, t=150),
            #             title=(f"""
            #             Intenção de voto 'geral' e de '{rel2}' por candidato segundo '{inst2.title()}' (2º turno)
            #             <br>
            #             <br>
            #             """),
            #                             xaxis_title='Mês, ano e instituto de pesquisa',
            #                             yaxis_title='Intenção de voto (%)',
            #                             font=dict(family="arial",size=13),
            #                             legend=dict(
            #                 yanchor="auto",
            #                 y=1.15,
            #                 xanchor="auto",
            #                 x=0.4,
            #                 orientation="h",
            #                 font_family="arial",))
            #     fig.update_xaxes(tickangle = 300,title_font_family="arial")
            #     fig.update_yaxes(range=[-0.5,95])

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source="https://cebrap.org.br/wp-content/themes/cebrap/images/logo-nav.png",
            #             xref="paper", yref="paper",
            #             x=1.05, y=1.03,
            #             sizex=0.1, sizey=0.1,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )

            #     # Add image
            #     fig.add_layout_image(
            #         dict(
            #             source=agre,
            #             xref="paper", yref="paper",
            #             x=1.05, y=1.08,
            #             sizex=0.12, sizey=0.12,
            #             xanchor="right", yanchor="bottom"
            #         )
            #     )
                
            #     st.plotly_chart(fig,use_container_width=True)
        
        st.markdown(f"""
        <h7 style='text-align: center; color:#606060;font-family:arial'>Nota 1: Os gráficos reproduzem os dados divulgados pelos institutos de pesquisa a partir do recorte religioso. Em alguns casos os institutos não coletam tais informações.</h7>
        <h7 style='text-align: center; color:#606060;font-family:arial'>Nota 2: Os gráficos com linhas descontinuadas indicam que o instituto não coletou a informação em determinada pesquisa. Um exemplo pode ser visto a partir da combinação "Paraná Pesquisas" e "católicos".</h7>
        """, unsafe_allow_html=True)

    st.markdown("---")



st.caption(f"""
<br>
<br>
Site publicado em: 15/05/2022.<br>
Última atualização: {end_date.strftime(format='%d/%m/%Y')}
""", unsafe_allow_html=True)