import streamlit as st
import pandas as pd
import datetime

# Configuração da página
st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit - Dashboard")

# URL da sua planilha em formato de exportação direta
# O segredo está no final: gid=0 (primeira aba) e format=csv
SHEET_URL = "https://docs.google.com/spreadsheets/d/1FUwTQoih5UrBn-4j_A9qmcbHoGCeha2UsIuPoMTiuRE/edit?usp=sharing"

def load_data():
    # Adicionamos um parâmetro de tempo para enganar o cache do navegador e do Google
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    full_url = f"{SHEET_URL}&t={timestamp}"
    
    # Tentativa de leitura robusta
    try:
        # Lemos a planilha ignorando o cache interno do Streamlit
        data = pd.read_csv(full_url)
        return data
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

# Criar um botão de atualização manual que limpa o cache
if st.button('🔄 Sincronizar com Planilha Agora'):
    st.cache_data.clear()
    st.rerun()

# Carregar os dados
df = load_data()

if df is not None:
    if not df.empty:
        st.success(f"Dados atualizados às {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Estilizando a tabela para ficar profissional
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={
                "Link": st.column_config.LinkColumn("Link do Reddit"),
                "Keyword": "Palavra-Chave",
                "Data": "Data do Alerta"
            }
        )
    else:
        st.warning("Conectamos à planilha, mas ela parece estar sem linhas preenchidas.")
        st.info("Dica: Verifique se o Zapier realmente escreveu os dados na primeira aba da planilha.")
else:
    st.error("Não foi possível carregar os dados. Verifique o link da planilha no código.")

st.divider()
st.caption("Sistema de Monitoramento Reddit - Atualização em Tempo Real")
