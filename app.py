import streamlit as st
import streamlit_authenticator as stauth

# ⚠️ Copiamos tudo de st.secrets para um dicionário mutável
config = {
    "credentials": {
        "usernames": {
            username: dict(user)
            for username, user in st.secrets["credentials"]["usernames"].items()
        }
    },
    "cookie": dict(st.secrets["cookie"]),
    "preauthorized": dict(st.secrets.get("preauthorized", {}))
}

# 🔐 Inicializa autenticação com o config copiado
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    cookie_expiry_days=int(config["cookie"]["expiry_days"]),
    preauthorized=config["preauthorized"]
)


# Tela de login na sidebar
name, authentication_status, username = authenticator.login(
    label="Login",
    location="sidebar"
)

# Verifica status de autenticação
if authentication_status is False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, faça login.")
elif authentication_status:
    # Exibe logout e saudação
    authenticator.logout("Sair", location="sidebar")
    st.success(f"Bem-vindo, {name} 👋")

    # Aqui começa seu app privado
    st.header("📋 Lançamento de Despesas")
    with st.form("form_lancamento"):
        data = st.date_input("Data")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
        comentarios = st.text_area("Comentários")
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Outros"])
        enviar = st.form_submit_button("Lançar")

    if enviar:
        st.success("✅ Lançamento registrado com sucesso!")
        # Aqui você adiciona a lógica de salvar no banco
