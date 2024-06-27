import streamlit as st
from components import SelectNucleo,SelectMembro
from utils import generate_pcp,get_analistas,calculate_projects_per_analyst,get_base,count_unique_projects
from graphs import pacingPCP,ProjPorMembro

def main():
    df_base = get_base()
    
    #Sidebar
    nucleofilter = SelectNucleo()
    nucleo = nucleofilter.render(st.sidebar,df_base)
    base_analista = get_analistas(df_base,nucleo)
    memberfilter = SelectMembro()
    membro = memberfilter.render(st.sidebar,base_analista)

    pacing_pcp = generate_pcp(df_base,nucleo,membro)
    pacing_pcp['Projetos por Analista'] = pacing_pcp['Projeto por Analista'].apply(calculate_projects_per_analyst)
    pacing_pcp['Número de Projetos Únicos'] = pacing_pcp['Projeto por Analista'].apply(count_unique_projects)


    pcpGraph = pacingPCP()
    pcpGraph.render(pacing_pcp)

    projmembro = ProjPorMembro()
    projmembro.render(pacing_pcp)


if __name__ == '__main__':
    main()