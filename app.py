import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Carrega configurações
with open("config_auth.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Inicializa autenticação
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
    preauthorized=config.get('preauthorized', {})
)

# Tela de login
name, authentication_status, username = authenticator.login(
    label="Login",
    location="sidebar"  # ou "main"
)

# Pós-login
if authentication_status:
    authenticator.logout("Sair", location="sidebar")
    st.success(f"Bem-vindo, {name}!")
    # Exibir o resto do app aqui

elif authentication_status is False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status is None:
    st.info("Por favor, faça login.")
