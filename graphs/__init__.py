import plotly.express as px
import streamlit as st


class pacingPCP:

    def __init__(self):
        pass

    def plot_pacing_data(self,df):
        fig = px.line(df, x='Data', y='Número de Projetos Únicos', title='Número de Projetos Executando por Dia',
                    labels={'Número de Projetos Únicos': 'Número de Projetos Executando', 'Data': 'Data'})
        return fig
    
    def render(self,df):
        st.title('Gráfico de Pacing de Projetos')
        st.write("Este gráfico mostra o número de projetos executando por dia.")

        fig = self.plot_pacing_data(df)
        st.plotly_chart(fig)


class ProjPorMembro:

    def __init__(self):
        pass

    def plot_pacing_data(self,df):
        fig = px.line(df, x='Data', y='Projetos por Analista', title='Média de Projetos Executados Por Dia',
                    labels={'Projetos por Analista': 'Projetos por Analista', 'Data': 'Data'})
        return fig
    
    def render(self,df):
        st.title('Gráfico de de Pacing de Média de Projetos por dia')
        st.write("Este gráfico mostra a média de projetos em execução por dia.")

        fig = self.plot_pacing_data(df)
        st.plotly_chart(fig)