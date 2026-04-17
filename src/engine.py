import logging
import os

class ATM:
    def __init__(self):
        self.cards = ["1234 5678 9012 3432", "9876 5432 5743 3523", "1111 2222 3333 4444", "5555 6666 7777 8888"]

        self.accounts = {
            "1234 5678 9012 3432" : {"balance": 129000000.00, "password": "1234"},
            "9876 5432 5743 3523" : {"balance": 500.00, "password": "5678"},
            "1111 2222 3333 4444" : {"balance": 2000.00, "password": "9012"},
            "5555 6666 7777 8888" : {"balance": 1500.00, "password": "4321"}
        }

        self.failed_attempts = {}
        self.blocked_list = []

    def available_cards(self):
        list_formatted = []
        for card in self.cards:
            password = self.accounts[card]['password']
            list_formatted.append(f"Cartão: {card}  |  Senha: {password}")

        return list_formatted
    
    def get_transactions(self, card_number):
        history = []
        log_file = "logs/atm.log"

        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()

                for line in lines:
                    if card_number in line and ("Depósito" in line or "Saque" in line):
                        history.append(line.strip())

        return history[-5:]

    def authentication_acc(self, card_number, password):
        if card_number in self.blocked_list:
            logging.error("Tentativa de acesso com cartão BLOQUEADO: {card_number}")
            return "BLOQUEADO"

        if card_number in self.accounts:
            if self.accounts[card_number]['password'] == password:
                self.failed_attempts[card_number] = 0
                return card_number
            
            else:
                count = self.failed_attempts.get(card_number, 0) + 1
                self.failed_attempts[card_number] = count
            
                logging.warning(f"Falha de autenticação para {card_number}. Tentativa {count}/3.")

                if count >= 3:
                    self.blocked_list.append(card_number)
                    logging.info(f"🛑 Cartão {card_number} foi BLOQUEADO por excesso de tentativas.")
                    return "BLOQUEADO"
                
                return None
            
        return None