import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit - Dashboard")

# --- COLOQUE O SEU LINK AQUI ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/edit?usp=sharing"

def extrair_link_reddit(texto):
    if not isinstance(texto, str): return ""
    links = re.findall(r'(https?://(?:www\.)?reddit\.com/[^\s]+)', texto)
    return links[0] if links else "Link não detectado"

def carregar_dados():
    # Garante que o link seja convertido para formato de download CSV
    if "edit" in URL_PLANILHA:
        url_csv = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
    else:
        url_csv = URL_PLANILHA
    
    try:
        # O parâmetro clear_cache não existe aqui, então usamos um truque de tempo ou apenas lemos
        df = pd.read_csv(url_csv)
        if not df.empty and 'Link' in df.columns:
            df['Link'] = df['Link'].apply(extrair_link_reddit)
        return df
    except Exception as e:
        return None

if st.button('🔄 Atualizar Dashboard'):
    df = carregar_dados()
    if df is not None and not df.empty:
        st.success(f"Encontrados {len(df)} alertas!")
        st.dataframe(
            df,
            column_config={
                "Link": st.column_config.LinkColumn("Link Direto", width="large"),
                "Keyword": st.column_config.TextColumn("Termo"),
                "Data": st.column_config.TextColumn("Data/Hora")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.error("O Streamlit não conseguiu ler os dados. Verifique se a planilha está 'Pública' (Qualquer pessoa com o link pode ler).")

st.info("Nota: Se a planilha tem dados e aqui não aparece, clique em 'Refresh' no navegador.")
