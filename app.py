import streamlit as st
import pandas as pd

# 1. Configuração da página conforme os docs
st.set_page_config(page_title="Operação Reddit")

st.title("🚀 Operação Reddit")

# 2. URL de exportação da sua planilha
SHEET_URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

# 3. Função de carregamento com cache (limpa a cada 10 minutos ou no botão)
@st.cache_data(ttl=600)
def load_data(url):
    df = pd.read_csv(url)
    return df

try:
    data = load_data(SHEET_URL)
    
    if not data.empty:
        st.write("### Alertas Recentes")
        st.dataframe(data, use_container_width=True)
    else:
        st.info("A planilha está conectada, mas não há dados novos.")

except Exception as e:
    st.error("Erro ao conectar com o Google Sheets.")
    st.exception(e)

# Botão para forçar a atualização manual
if st.button("Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()
