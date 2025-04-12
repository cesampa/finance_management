import streamlit as st
from datetime import date
from db import init_db, Lancamento
from config import ALLOWED_USERS
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os
import pathlib
import cachetools
import requests
import streamlit_authenticator as stauth
import yaml

with open("config_auth.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Bem-vindo, {name}")
    # Exibir formulário
    ...
else:
    st.error("Usuário ou senha inválidos")

@st.cache_resource
def get_db():
    return init_db()

def get_last_saldo(session):
    last = session.query(Lancamento).order_by(Lancamento.id.desc()).first()
    return last.saldo if last else 0.0

def main():
    st.set_page_config(page_title="Controle Financeiro", layout="centered")
    st.title("💰 Controle Financeiro Pessoal")


    if novo_saldo < 0:
        st.error("⚠️ Saldo negativo! Atenção com os gastos.")
    elif novo_saldo < 100:
        st.warning("🔔 Saldo abaixo de R$ 100, cuidado!")
    else:
        st.info("✅ Saldo positivo e saudável.")


    session = get_db()

    with st.form("form-lancamento"):
        data = st.date_input("Data", date.today())
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", step=0.01)
        comentarios = st.text_area("Comentários")

        submitted = st.form_submit_button("Registrar")

        if submitted:
            saldo_anterior = get_last_saldo(session)
            novo_saldo = saldo_anterior - valor
            lanc = Lancamento(
                data=data,
                descricao=descricao,
                valor=valor,
                comentarios=comentarios,
                saldo=novo_saldo
            )
            session.add(lanc)
            session.commit()
            st.success(f"Lançamento registrado com sucesso. Saldo atual: R$ {novo_saldo:.2f}")

    # Exibir histórico
    st.subheader("📜 Histórico")
    rows = session.query(Lancamento).order_by(Lancamento.id.desc()).limit(10).all()
    if rows:
        st.table([{
            "Data": r.data,
            "Descrição": r.descricao,
            "Valor (R$)": r.valor,
            "Saldo (R$)": r.saldo,
            "Comentários": r.comentarios
        } for r in rows])
    else:
        st.info("Nenhum lançamento ainda.")

# === Google OAuth Login ===
def authenticate_user():
    if "credentials" not in st.session_state:
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={st.secrets['google_client_id']}"
            f"&response_type=token"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope={' '.join(SCOPES)}"
        )
        st.markdown(f"[Login com Google]({auth_url})")
    else:
        token_info = st.session_state.credentials
        idinfo = id_token.verify_oauth2_token(token_info['id_token'], requests.Request())
        email = idinfo.get('email')

        if email in ALLOWED_USERS:
            st.session_state.user_email = email
        else:
            st.error("Acesso negado. Sua conta não está autorizada.")

if __name__ == "__main__":
    main()
