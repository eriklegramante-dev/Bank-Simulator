class ATM:
    def __init__(self):
        self.cards = ["1234 5678 9012 3432", "9876 5432 5743 3523", "1111 2222 3333 4444", "5555 6666 7777 8888"]

        self.accounts = {
            "1234 5678 9012 3432" : {"balance": 1000.0, "password": "1234"},
            "9876 5432 5743 3523" : {"balance": 500.0, "password": "5678"},
            "1111 2222 3333 4444" : {"balance": 2000.0, "password": "9012"},
            "5555 6666 7777 8888" : {"balance": 1500.0, "password": "4321"}
        }

    def available_cards(self):
        list_formatted = []
        for card in self.cards:
            password = self.accounts[card]['password']
            list_formatted.append(f"Cartão: {card}  |  Senha: {password}")

        return list_formatted

    def blocked_cards(self): 
        blocked_cards_list = []
        return blocked_cards_list


    def authentication_acc(self):
        attempts_blocking = 3

        while True:
            card_number = input("Digite o número do cartão:")
            password = input("Digite a senha:")

            if card_number in self.cards and self.accounts[card_number]['password'] == password:
                print("Autenticação bem-sucedida!")
                return card_number
            
            elif card_number in self.blocked_cards():
                print("Número do cartão ou senha incorretos.")
                attempts_blocking -= 1
                if attempts_blocking == 0:
                    print("Número do cartão bloqueado. Tente novamente mais tarde.")
                    return None
                continue

            else:
                print("Informações incorretas. Tente novamente.")
                continue
