import logging
#import time
import streamlit as st

from engine import ATM

logging.basicConfig(level=logging.INFO)
logging.info("Iniciando o caixa eletrônico...")

st.set_page_config(page_title="Caixa Eletrônico", layout="centered")
atm = ATM()

#simulador de logs "iniciando o caixa eletrônico"
with st.container(border=True):
    st.title("🏦 Bem vindo ao Banco Naster!")

    with st.container(border=True):
        st.subheader("Cartões Disponíveis para simular o acesso:")
        cards = st.selectbox("Selecione um cartão: ",atm.available_cards())
        if cards:
            st.write(f"Você selecionou o cartão: {cards}")

    with st.container(border=True):
        st.subheader("Autenticação:")
        st.write("Digite o número do cartão e a senha para autenticar.")
        card_number = st.text_input("Número do cartão:")
        password = st.text_input("Senha:", type="password")

        if st.button("Autenticar"):
            pass