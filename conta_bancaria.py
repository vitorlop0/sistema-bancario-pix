import os
import json
from datetime import datetime
from pix_utils import gerar_qrcode

class ContaBancaria:

    def __init__(self):
        self.caminho_arquivo = "dados_banco.json"
        self.saldo = 0
        self.extrato = []
        self.carregar_dados()

    
    def mostrar_saldo(self):
         print(f"Seu saldo é de {self.saldo:.2f}")

    def fazer_pix(self):
        while True:
            try:
                valor_pix = float(input("Valor do pix: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if valor_pix <= 0:
                print("O valor do PIX deve ser maior que 0.")
                continue

            if valor_pix > self.saldo:
                print("Valor não disponível em conta, verifique seu saldo.")
                continue

            gerar_qrcode(valor_pix)
            self.saldo -= valor_pix
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
            print(f"PIX de {valor_pix:.2f} realizado com sucesso!")
            print(f"Seu novo saldo é: R$ {self.saldo:.2f}")

            self.extrato.append({
                "tipo": "PIX ENVIADO",
                "valor": valor_pix,
                "data": data_hora
            })

            with open(self.caminho_arquivo, "w") as arquivo:
                json.dump({"saldo": self.saldo, "extrato": self.extrato}, arquivo)

            break


    def adicionar_saldo(self):
        while True:
            try:
                valor_adicionado = float(input("Digite um valor: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if valor_adicionado <= 0:
                print("O valor deve ser maior que 0!")
                continue

            self.saldo += valor_adicionado
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
            print(f"Seu novo saldo: R$ {self.saldo:.2f}")
            self.extrato.append({
                "tipo": "DEPÓSITO",
                "valor": valor_adicionado,
                "data": data_hora
            })

            with open(self.caminho_arquivo, "w") as arquivo:
                json.dump({"saldo": self.saldo, "extrato": self.extrato}, arquivo)

            break


    def mostrar_extrato(self):
        print("----- Extrato Bancário ----- ")

        if not self.extrato:
            print("Nenhuma movimentação realizada ainda.")
        

        else:
            for movimentacao in self.extrato:
                tipo = movimentacao["tipo"]
                valor = movimentacao["valor"]
                data = movimentacao["data"]

                print(f"{tipo}: R$ {valor:.2f} - Data: {data}")

    def somar_pix(self):

        soma = 0

        for movimentacao in self.extrato:

            if movimentacao["tipo"] == "PIX ENVIADO":
                soma += movimentacao["valor"]

        print(f"Soma de pix enviados: R$ {soma:.2f} ")

    
    def carregar_dados(self):
        if os.path.exists(self.caminho_arquivo):
            try:
                with open(self.caminho_arquivo, "r") as arquivo:
                    dados = json.load(arquivo)
                    self.saldo = dados["saldo"]
                    self.extrato = dados["extrato"]

            except:
                self.saldo = 0
                self.extrato = []
                with open(self.caminho_arquivo, "w") as arquivo:
                    json.dump({"saldo": self.saldo, "extrato": self.extrato}, arquivo)

        else:
            self.saldo = 0
            self.extrato = []
            with open(self.caminho_arquivo, "w") as arquivo:
                json.dump({"saldo": self.saldo, "extrato": self.extrato}, arquivo)