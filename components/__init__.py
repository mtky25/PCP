import streamlit as st

class SelectNucleo:
    
    def __init__(self):
        pass

    def render(self,st,df_base):
        nucleo_selected = st.selectbox("Escolha o Núcleo",df_base['Núcleo'].unique(),index=None)
        return nucleo_selected
    

class SelectMembro:
    
    def __init__(self):
        pass

    def render(self,st,base_analista):
        membro_selected = st.selectbox("Escolha o Núcleo",base_analista['Analista'].unique(),index=None)
        return membro_selected