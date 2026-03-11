import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit - Dashboard")
st.write("Visualização em tempo real dos alertas capturados via Planilha.")

# MANTENHA O SEU LINK DA PLANILHA AQUI
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/edit?pli=1&gid=0#gid=0"

if "edit" in URL_PLANILHA:
    URL_CSV = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    URL_CSV = URL_PLANILHA

def extrair_link(texto):
    # Procura um link que contenha 'reddit.com' dentro do textão que o Zapier envia
    if not isinstance(texto, str):
        return texto
    links = re.findall(r'(https?://[^\s]+reddit\.com[^\s]+)', texto)
    return links[0] if links else texto

def carregar_data():
    try:
        df = pd.read_csv(URL_CSV)
        if not df.empty and 'Link' in df.columns:
            # Limpa o texto vindo do Zapier para deixar só o link
            df['Link'] = df['Link'].apply(extrair_link)
        return df
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return pd.DataFrame()

if st.button('🔄 Atualizar Dashboard'):
    with st.spinner('Buscando novos dados...'):
        df = carregar_data()
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "Link": st.column_config.LinkColumn("Ir para o Reddit", width="medium")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("A planilha está vazia ou ainda não recebeu dados do Zapier.")

st.info("O Zapier agora está monitorando seu e-mail e alimentando esta lista automaticamente.")
