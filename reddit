import streamlit as st
import imaplib
import email
from email.header import decode_header
import re
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Reddit Monitor", layout="wide")

st.title("🚀 Operação Reddit")
st.write("Fila de interações baseada nos alertas do F5Bot.")

def check_alerts():
    alerts = []
    try:
        # Puxa os dados dos Secrets que você já configurou no Streamlit
        mail = imaplib.IMAP4_SSL(st.secrets["IMAP_SERVER"])
        mail.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
        mail.select("inbox")

        # Busca e-mails do F5Bot
        status, messages = mail.search(None, '(FROM "noreply@f5bot.com")')
        mail_ids = messages[0].split()[-15:] # Pega os últimos 15 e-mails
        
        for m_id in reversed(mail_ids):
            res, msg_data = mail.fetch(m_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    keyword = subject.replace("F5Bot alert: ", "")
                    
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()

                    links = re.findall(r'(https?://(?:www\.)?reddit\.com/r/[^\s]+)', body)
                    reddit_link = links[0] if links else "Link não encontrado"
                    
                    alerts.append({
                        "Keyword": keyword,
                        "Link": reddit_link,
                        "Data": msg["Date"]
                    })
        mail.close()
        mail.logout()
    except Exception as e:
        st.error(f"Erro: {e}. Verifique se a Senha de Aplicativo está correta.")
    return alerts

if st.button('🔄 Atualizar Fila'):
    with st.spinner('Lendo e-mails...'):
        data = check_alerts()
        if data:
            df = pd.DataFrame(data)
            st.data_editor(
                df,
                column_config={"Link": st.column_config.LinkColumn("Abrir no Reddit")},
                hide_index=True, use_container_width=True
            )
        else:
            st.warning("Nenhum alerta encontrado na caixa de entrada.")
