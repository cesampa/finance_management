import streamlit as st
import streamlit_authenticator as stauth

# Copia as configurações para um dicionário mutável
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

# Autenticador
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    cookie_expiry_days=int(config["cookie"]["expiry_days"]),
    preauthorized=config["preauthorized"]
)

# Login
name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status is False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, realize o login.")
elif authentication_status:
    authenticator.logout("Sair", "sidebar")
    st.success(f"Bem-vindo, {name}! ✅")
    st.write("🔒 Área protegida do app")


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
