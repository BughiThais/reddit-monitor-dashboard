import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Monitor Reddit", layout="wide")

st.title("🚀 Operação Reddit")

# Link direto da sua planilha
URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

try:
    # Força o Google a não usar cache com o carimbo de tempo
    df = pd.read_csv(f"{URL}&t={time.time()}")
    
    if not df.empty:
        st.success(f"Dashboard atualizado! {len(df)} alertas encontrados.")
        # Exibe os dados de forma simples para não ter erro de formatação
        st.write(df)
    else:
        st.warning("A planilha está conectada, mas não há dados nas linhas.")

except Exception as e:
    st.error("Erro ao ler a planilha.")
    st.info(f"Detalhe técnico: {e}")

if st.button('🔄 Forçar Atualização'):
    st.rerun()
