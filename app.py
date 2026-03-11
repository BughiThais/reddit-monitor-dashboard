import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit - Dashboard")

# SUBSTITUA PELO SEU LINK DA PLANILHA (Certifique-se de que está pública para leitura)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/edit?usp=sharing"

def extrair_link_reddit(texto):
    if not isinstance(texto, str):
        return ""
    # Esta linha procura especificamente por links do reddit no meio do texto
    links = re.findall(r'(https?://(?:www\.)?reddit\.com/[^\s]+)', texto)
    return links[0] if links else "Link não detectado"

def carregar_dados():
    if "edit" in URL_PLANILHA:
        url_csv = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
    else:
        url_csv = URL_PLANILHA
    
    try:
        df = pd.read_csv(url_csv)
        # Se a coluna 'Link' existir, vamos limpá-la
        if 'Link' in df.columns:
            df['Link'] = df['Link'].apply(extrair_link_reddit)
        return df
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return pd.DataFrame()

if st.button('🔄 Atualizar Dashboard'):
    with st.spinner('Lendo planilha...'):
        df = carregar_dados()
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "Link": st.column_config.LinkColumn("Link Direto", width="large"),
                    "Keyword": st.column_config.TextColumn("Termo")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado encontrado. Verifique se o Zapier já preencheu a planilha.")

st.info("Configurado: O Dashboard agora limpa o texto do e-mail e mostra apenas o link do Reddit.")
