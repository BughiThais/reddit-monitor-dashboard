import streamlit as st
import imaplib
import email
from email.header import decode_header
import pandas as pd
import re

# CONFIGURAÇÕES DIRETO NO CÓDIGO (Para resolver o erro de conexão)
EMAIL_USER = "thais.bughi@monsterd.com.br"
EMAIL_PASS = "bdfvxofassdpxjnx"
IMAP_SERVER = "outlook.office365.com"

st.set_page_config(page_title="Operação Reddit", layout="wide")

st.title("🚀 Operação Reddit - F5Bot")
st.write("Fila de atendimento baseada nos alertas do e-mail.")

def buscar_emails():
    try:
        # Conexão
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Busca e-mails do F5Bot
        status, messages = mail.search(None, '(FROM "noreply@f5bot.com")')
        email_ids = messages[0].split()

        dados = []
        # Pega os últimos 20 e-mails
        for i in range(len(email_ids), max(0, len(email_ids)-20), -1):
            res, msg = mail.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Extrair corpo para achar o link
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # Achar link do Reddit usando Regex
                    links = re.findall(r'(https?://[^\s]+reddit\.com[^\s]+)', body)
                    link_final = links[0] if links else "Link não encontrado"
                    
                    # Tenta extrair a Keyword do assunto
                    keyword = subject.replace("F5Bot: ", "")

                    dados.append({
                        "Keyword": keyword,
                        "Link": link_final,
                        "Data": msg["Date"]
                    })
        
        mail.logout()
        return pd.DataFrame(dados)
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return pd.DataFrame()

if st.button('🔄 Atualizar Fila'):
    with st.spinner('Consultando e-mails...'):
        df = buscar_emails()
        if not df.empty:
            # Torna o link clicável
            st.dataframe(
                df,
                column_config={
                    "Link": st.column_config.LinkColumn("Ir para o Reddit")
                },
                hide_index=True,
            )
        else:
            st.warning("Nenhum alerta encontrado na caixa de entrada.")

st.info("Dica: Os alertas aparecem aqui conforme o F5Bot envia os e-mails para thais.bughi@monsterd.com.br")
