import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit")

# Link direto para exportação
URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

# Botão para forçar a atualização
if st.button('🔄 Atualizar Dados'):
    st.cache_data.clear()

try:
    # O truque do time.time() evita que o Google entregue uma versão velha/vazia
    url_final = f"{URL}&t={time.time()}"
    df = pd.read_csv(url_final)

    if not df.empty:
        st.success(f"Encontramos {len(df)} linhas na planilha!")
        # Mostra a tabela completa
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("A planilha foi encontrada, mas parece não ter dados nas linhas.")

except Exception as e:
    st.error(f"Erro na leitura: {e}")

st.info("Nota: Verifique se os dados na sua Planilha Google começam na Linha 1.")
