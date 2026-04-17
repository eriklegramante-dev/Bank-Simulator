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
            card_number = st.text_input("💳 Número do cartão:").rstrip()
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
                        logging.warning("Falha de autenticação.")

    st.write("Dica: Use os cartões disponíveis para simular o acesso. Após 3 tentativas falhas, o cartão será bloqueado.")
    st.write("Exemplo de cartão: '1234 5678 9012 3432' com senha '1234'.")
    st.write("Além do cartão que usará para realizar o acesso, salve outro cartão para testar a funcionalidade de transferência.")

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
                if st.button("📄 Extrato", use_container_width=True):
                    st.session_state.current_operation = "Extrato"
                    logging.info(f"Operação selecionada: Extrato para {st.session_state.active_card}.")

            st.divider()

            if st.session_state.current_operation == "Saque":
                with st.container(border=True):
                    st.subheader("💸 Área de Saque")
                    amount = st.number_input("Valor do Saque:", min_value=0.0, step=10.0)

                    if amount > saldo:
                        st.error("⚠️ Saldo insuficiente para este saque.")

                    conf_password = st.text_input("🔑 Confirme sua senha:", type="password")
                    
                    if st.button("Confirmar Saque", use_container_width=True):
                        corr_password = atm.accounts[st.session_state.active_card]['password']

                        if corr_password != conf_password:
                            st.error("❌ Senha incorreta. Saque cancelado.")
                            logging.warning(f"Saque cancelado por senha incorreta para {st.session_state.active_card}.")
                        elif amount <= 0:
                            st.warning("⚠️ Digite um valor válido para saque.")
                        elif amount > saldo:
                            st.error("⚠️ Saldo insuficiente para este saque.")
                        else:
                            new_balance = saldo - amount
                            atm.accounts[st.session_state.active_card]['balance'] = new_balance

                            st.success(f"Saque de R$ {amount:,.2f} realizado com sucesso!")
                            logging.info(f"Saque de R$ {amount:,.2f} realizado para {st.session_state.active_card}. Novo saldo: R$ {new_balance:,.2f}.")

                            time.sleep(1.5)
                            st.session_state.current_operation = None
                            st.rerun()

            if st.session_state.current_operation == "Transferência":
                with st.container(border=True):
                    st.subheader("📲 Área de Transferência")
                    recipient = st.text_input("Número do cartão destinatário: ").rstrip()

                    amount = st.number_input("Valor da Transferência:", min_value=0.0, step=10.0)
                    if amount > saldo:
                        st.error("⚠️ Saldo insuficiente para esta transferência.")

                    conf_password = st.text_input("🔑 Confirme sua senha:", type="password")

                    if st.button("Confirmar Transferência", use_container_width=True):
                        corr_password = atm.accounts[st.session_state.active_card]['password']

                        if corr_password != conf_password:
                            st.error("❌ Senha incorreta. Transferência cancelada.")
                            logging.warning(f"Transferência cancelada por senha incorreta para {st.session_state.active_card}.")

                        elif recipient not in atm.accounts:
                            st.error("❌ Cartão destinatário não encontrado. Transferência cancelada.")
                            logging.warning(f"Transferência cancelada por destinatário inválido: {recipient}.")
                        
                        elif amount <= 0:
                            st.warning("⚠️ Digite um valor válido para transferência.")
                        
                        elif amount > saldo:
                            st.error("⚠️ Saldo insuficiente para esta transferência.")

                        else:
                            atm.accounts[st.session_state.active_card]['balance'] -= amount
                            atm.accounts[recipient]['balance'] += amount
                            res_sender = atm.accounts[st.session_state.active_card]['balance']
                            res_recipient = atm.accounts[recipient]['balance']

                            logging.info(f"Sucesso: {st.session_state.active_card} enviou R${amount} para {recipient}.")
                            logging.info(f"Novos Saldos -> Remetente: {res_sender} | Destinatário: {res_recipient}")

                            st.success(f"Transferência de R$ {amount:,.2f} realizada!")
                            time.sleep(3)

                            st.session_state.current_operation = None
                            st.rerun()

            if st.session_state.current_operation == "Extrato":
                with st.container(border=True):
                    st.subheader("📄 Extrato de Transações")
                    st.write(f"Últimas 5 transações (Depósitos e Saques): **{st.session_state.active_card}**")

                    log_path = "logs/atm.log"
                    if os.path.exists(log_path):
                        with open(log_path, "r") as f:
                            moviments = [line for line in f.readlines() if st.session_state.active_card in line]

                            if moviments:
                                for mov in reversed(moviments[-5:]):
                                    st.code(mov, language="text")
                            else:
                                st.info("Nenhuma movimentação encontrada para este cartão.")
                    else:
                        st.error("Arquivo de log não encontrado. Nenhuma movimentação disponível.")

                    if st.button("Fechar Extrato", use_container_width=True):
                        st.session_state.current_operation = None
                        st.rerun()

                    

        st.divider()
        
        if st.button("Encerrar Sessão", use_container_width=True):
            logging.info(f"Sessão encerrada para {st.session_state.active_card}.")
            st.session_state.authenticated = False
            st.session_state.active_card = None
            st.rerun()