import logging
import time
import os
import streamlit as st

from engine import ATM

log_dir = "logs"
log_file = os.path.join(log_dir, "atm.log")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()])

st.set_page_config(page_title="Caixa Eletrônico", layout="centered")

if 'atm' not in st.session_state:
    st.session_state.atm = ATM()

atm = st.session_state.atm

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_card" not in st.session_state:
    st.session_state.active_card = None

if "current_operation" not in st.session_state:
    st.session_state.current_operation = None


if not st.session_state.authenticated:
    with st.container(border=True):
        st.title("🏦 Bem vindo ao Banco Naster!")

        with st.container(border=True):
            st.subheader("Cartões Disponíveis para simular o acesso:")
            cards = st.selectbox("Selecione um cartão: ", atm.available_cards())
            if cards:
                st.write(f"Você selecionou o cartão: {cards}")

        with st.container(border=True):
            st.subheader("Autenticação:")
            card_number = st.text_input("💳 Número do cartão:")
            password = st.text_input("🔑 Senha:", type="password")

            if st.button("Autenticar", use_container_width=True):
                with st.spinner("Autenticando..."):
                    time.sleep(1.5)
                    authenticated_card = atm.authentication_acc(card_number, password)
                    logging.info(f"Autenticação bem-sucedida para {card_number}.")
                    
                    if authenticated_card == "BLOQUEADO":
                        st.error("⚠️ Cartão BLOQUEADO devido a múltiplas tentativas falhas.")
                    
                    elif authenticated_card:
                        st.success("✅ Autenticação bem-sucedida!")
                        st.session_state.authenticated = True
                        st.session_state.active_card = authenticated_card
                        st.rerun()

                    else:
                        st.error("❌ Falha na autenticação. Verifique o número do cartão e a senha.")

else:
    with st.container(border=True):
        st.title(f"🏦 Painel da Conta")
        st.success(f"Acesso autorizado: {st.session_state.active_card}")
        
        saldo = atm.accounts[st.session_state.active_card]['balance']
        st.metric("Saldo Atual", f"R$ {saldo:,.2f}")
        
        with st.container(border=True):
            st.title("🏦 Painel de Operações")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("💸 Saque", use_container_width=True):
                    st.session_state.current_operation = "Saque"
                    logging.info(f"Operação selecionada: Saque para {st.session_state.active_card}.")

            with col2:
                if st.button("📲 Transferência", use_container_width=True):
                    st.session_state.current_operation = "Transferência"
                    logging.info(f"Operação selecionada: Transferência para {st.session_state.active_card}.")

            with col3:
                if st.button("💰 Depósito", use_container_width=True):
                    st.session_state.current_operation = "Depósito"
                    logging.info(f"Operação selecionada: Depósito para {st.session_state.active_card}.")

            st.divider()

            if st.session_state.current_operation == "Saque":
                with st.container(border=True):
                    st.subheader("💸 Área de Saque")
                    amount = st.number_input("Valor do Saque:", min_value=0.0, step=10.0)
                    if st.button("Confirmar Saque", use_container_width=True):
                        st.success(f"Saque de R$ {amount:,.2f} realizado com sucesso!")
                        st.session_state.current_operation = None
                        st.rerun()


        st.divider()
        
        if st.button("Encerrar Sessão", use_container_width=True):
            logging.info(f"Sessão encerrada para {st.session_state.active_card}.")
            st.session_state.authenticated = False
            st.session_state.active_card = None
            st.rerun()