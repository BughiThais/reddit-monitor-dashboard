import streamlit as st
import pandas as pd

# 1. Configuração simples
st.set_page_config(page_title="Monitor Reddit", layout="wide")
st.title("🚀 Operação Reddit")

# 2. Link da sua planilha (ajustado para exportação)
URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

# 3. Função de leitura
try:
    # Lendo a planilha direto
    df = pd.read_csv(URL)
    
    if not df.empty:
        st.success("Dados carregados com sucesso!")
        # Exibe a tabela bruta para garantir que estamos vendo tudo
        st.write(df)
    else:
        st.warning("A planilha está conectada, mas não tem dados.")
except Exception as e:
    st.error("Erro crítico de conexão.")
    st.info(f"O erro é: {e}")

# 4. Botão de Refresh
if st.button('🔄 Atualizar Agora'):
    st.rerun()
