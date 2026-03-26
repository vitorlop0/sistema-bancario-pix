import qrcode
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

def calcular_crc16(payload):
    # Essa é a fórmula matemática padrão exigida pelo Banco Central para o PIX (método criado com ajuda de IA)
    crc = 0xFFFF
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def gerar_qrcode(valor_pix):
    print("\n[Sistema] Montando código PIX dinâmico...")

    nome = os.getenv("MEU_NOME")
    cidade = os.getenv("MINHA_CIDADE")
    chave = os.getenv("MINHA_CHAVE")

    tam_nome = f"{len(nome):02d}"
    tam_cidade = f"{len(cidade):02d}"
    tam_chave = f"{len(chave):02d}"

    # 1. Formatamos o valor para ter sempre 2 casas decimais (ex: 50.50)
    str_valor = f"{valor_pix:.2f}"
    
    # 2. Descobrimos o tamanho desse valor (ex: "50.50" tem 5 caracteres, então vira "05")
    tamanho_valor = f"{len(str_valor):02d}"

    # 3. Montamos o bloquinho do dinheiro (ID 54 + Tamanho + Valor)
    bloco_valor = f"54{tamanho_valor}{str_valor}"

    # 4. Juntamos tudo (Seus dados + o bloco de dinheiro dinâmico)
    # Note que termina em "6304", que é o aviso pro banco de que a assinatura vem logo depois
    payload = (
        f"00020101021126360014br.gov.bcb.pix01{tam_chave}{chave}520400005303986" +
        bloco_valor +
        f"5802BR59{tam_nome}{nome}60{tam_cidade}{cidade}62070503***6304"
    )

    # 5. Calculamos a assinatura de segurança em cima desse texto novo
    assinatura_crc16 = calcular_crc16(payload)

    # 6. O texto final que vai pro QR Code é o texto base + a assinatura matemática
    texto_pix = payload + assinatura_crc16

    # Gera a imagem
    img_qr = qrcode.make(texto_pix)
    img_qr.save("qr_code_gerado.png")

    print("[Sistema] QR CODE dinâmico gerado com sucesso!")

caminho_arquivo = "dados_banco.json"


 # se o arquivo json existe, ele é aberto em modo leitura e depois o json é transformado em um dicionário
if os.path.exists(caminho_arquivo):

    try:
        with open (caminho_arquivo, "r") as arquivo:

        
            dados = json.load(arquivo) # var dados ler todas as linhas e vira um dicionário
            saldo = dados["saldo"] # saldo recebe o valor da chave "saldo"
            extrato = dados["extrato"] # extrato recebe o valor da chave "extrato"

    except:
            saldo = 0
            extrato = []
            with open (caminho_arquivo, "w") as arquivo:
                json.dump({"saldo": saldo, "extrato": extrato}, arquivo)


# se o arquivo json não existe na inicialização, ele é criado aqui
else:
    saldo = 0
    extrato = []

    with open (caminho_arquivo, "w") as arquivo:
        json.dump({"saldo": saldo, "extrato": extrato}, arquivo) # json.dump transforma dicionário em json


print("********************* Sistema bancário de PIX *********************")

while(True):
    print("\n--- MEU BANCO DIGITAL ---")
    print("1 - Ver Saldo")
    print("2 - Fazer PIX")
    print("3 - Adicionar saldo")
    print("4 - Ver extrato")
    print("5 - Somar pix enviados")
    print("6 - Sair")

    opcao = input("Selecione uma das opções: ")

    if opcao == "1":
        print(f"Seu saldo atual é: {saldo:.2f}")

    elif opcao == "2":
        valor_pix = float(input("Valor do pix: "))

        if valor_pix <= saldo:

            gerar_qrcode(valor_pix)
            saldo = saldo - valor_pix
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
            print(f"PIX de {valor_pix:.2f} realizado com sucesso!")
            print(f"Seu novo saldo é: R$ {saldo:.2f}")

            extrato.append({
                "tipo": "PIX ENVIADO",
                "valor": valor_pix,
                "data": data_hora
            })

            with open(caminho_arquivo, "w") as arquivo:
                json.dump({"saldo": saldo, "extrato": extrato}, arquivo)

        else:
            print("Valor não disponível em conta, verifique seu saldo.")

    elif opcao == "3":

        while True:
            valor_adicionado = float(input("Digite um valor: "))

            if valor_adicionado > 0:
                saldo = saldo + valor_adicionado
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
                print(f"Seu novo saldo: R$ {saldo:.2f}")
                extrato.append({
                    "tipo": "DEPÓSITO",
                    "valor": valor_adicionado,
                    "data": data_hora

                })

                with open(caminho_arquivo, "w") as arquivo:
                    json.dump({"saldo": saldo, "extrato": extrato}, arquivo)

                break

            else:
                print("O valor deve ser maior que 0!")

    
    elif opcao == "4":

        print("----- Extrato Bancário ----- ")

        if len(extrato) == 0:
            print("Nenhuma movimentação realizada ainda.")
        

        else:
            for movimentacao in extrato:
                tipo = movimentacao["tipo"]
                valor = movimentacao["valor"]
                data = movimentacao["data"]

                print(f"{tipo}: R$ {valor:.2f} - Data: {data}")

    elif opcao == "5":

        soma = 0

        for movimentacao in extrato:

            if movimentacao["tipo"] == "PIX ENVIADO":
                soma = soma + movimentacao["valor"]

        print(f"Soma de pix enviados: R$ {soma:.2f} ")

    elif opcao == "6":
        print("Encerrando o sistema!")
        break

    else:
        print("Opção inválida!")