import streamlit as st
import pandas as pd
import re
import time

st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit - Dashboard")

# Link da sua planilha já configurado
URL_BASE = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/export?format=csv"

def extrair_link_reddit(texto):
    if not isinstance(texto, str): return ""
    # Busca por links do reddit no texto vindo do Zapier
    links = re.findall(r'(https?://(?:www\.)?reddit\.com/[^\s]+)', texto)
    if links:
        # Remove caracteres residuais como parênteses ou aspas no fim do link
        return links[0].replace(')', '').replace('"', '').replace('>', '')
    return "Link não detectado"

def carregar_dados():
    try:
        # O 'time.time' gera um número diferente toda vez, forçando o Google a atualizar os dados
        url_dinamica = f"{URL_BASE}&t={time.time()}"
        df = pd.read_csv(url_dinamica)
        
        if not df.empty:
            # Garante que as colunas existem antes de tratar
            if 'Link' in df.columns:
                df['Link'] = df['Link'].apply(extrair_link_reddit)
        return df
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return pd.DataFrame()

# Botão de atualização
if st.button('🔄 Atualizar Dashboard Agora'):
    with st.spinner('Buscando dados novos na planilha...'):
        # Limpa o cache do Streamlit antes de ler
        st.cache_data.clear()
        df = carregar_dados()
        
        if not df.empty:
            st.success(f"Sucesso! {len(df)} alertas encontrados.")
            st.dataframe(
                df,
                column_config={
                    "Link": st.column_config.LinkColumn("Link do Reddit", width="large"),
                    "Keyword": st.column_config.TextColumn("Termo"),
                    "Data": st.column_config.TextColumn("Data do Alerta")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("A planilha parece estar vazia ou o Streamlit não conseguiu acessá-la.")

st.info("Dica: Se você acabou de ver o dado entrar na Planilha Google, aguarde 5 segundos e clique no botão acima.")
