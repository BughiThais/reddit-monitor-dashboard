import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Teste Final", layout="wide")

# Link direto para exportação CSV da sua planilha
URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

st.title("🔎 Teste de Conexão")

# Força a limpeza de cache toda vez que rodar
st.cache_data.clear()

try:
    # Adicionamos um número aleatório no fim do link para o Google não enviar versão antiga
    url_final = f"{URL}&t={time.time()}"
    df = pd.read_csv(url_final)
    
    st.success("Conexão com a planilha OK!")
    st.write("Dados encontrados:")
    st.write(df) # Isso vai mostrar a tabela crua, sem frescura

except Exception as e:
    st.error(f"O Streamlit não conseguiu ler a planilha.")
    st.info(f"Erro técnico: {e}")

if st.button('Tentar ler novamente'):
    st.rerun()
