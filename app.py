import os
import subprocess
import sys

# Força a instalação do pandas se ele não for encontrado
try:
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

import streamlit as st
import time

st.set_page_config(page_title="Dashboard Reddit", layout="wide")

st.title("🚀 Monitoramento Reddit & Zapier")

# URL da sua planilha (formato CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

def carregar_dados():
    # Adicionamos um timestamp para evitar cache do Google
    url = f"{SHEET_URL}&cache={int(time.time())}"
    return pd.read_csv(url)

try:
    df = carregar_dados()
    
    if not df.empty:
        st.success(f"Conectado com sucesso! {len(df)} alertas registrados.")
        
        # Formatação para o Zapier: Se a coluna 'Link' existir, tentamos limpar
        if 'Link' in df.columns:
            st.dataframe(
                df, 
                column_config={"Link": st.column_config.LinkColumn("Link do Alerta")},
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write(df)
    else:
        st.warning("A planilha foi lida, mas parece estar vazia. O Zapier já enviou dados para lá?")

except Exception as e:
    st.error("Erro na integração.")
    st.info(f"O Streamlit não conseguiu ler os dados. Verifique se a planilha está 'Pública para qualquer pessoa com o link'.")
    st.debug(f"Detalhes: {e}")

if st.button('🔄 Sincronizar Agora'):
    st.rerun()
