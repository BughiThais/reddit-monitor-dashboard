import streamlit as st
import pandas as pd

st.set_page_config(page_title="Operação Reddit", layout="wide")
st.title("🚀 Operação Reddit")

# Link direto para exportação da sua planilha
URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

try:
    # Lendo a planilha sem frescuras
    df = pd.read_csv(URL)
    
    if not df.empty:
        st.success(f"Conectado! Encontramos {len(df)} alertas.")
        st.write("Abaixo estão os dados da sua planilha:")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Conectado à planilha, mas ela está vazia. Verifique se o Zapier preencheu algo.")

except Exception as e:
    st.error("Erro ao ler a planilha.")
    st.info(f"Detalhe do erro: {e}")

if st.button('🔄 Forçar Atualização'):
    st.rerun()
