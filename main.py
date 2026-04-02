from conta_bancaria import ContaBancaria
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

def main():
    # Instancia a conta bancária, que já carrega os dados automaticamente
    conta = ContaBancaria()

    print("********************* Sistema bancário de PIX *********************")

    while True:
        print("\n--- MEU BANCO DIGITAL ---")
        print("1 - Ver Saldo")
        print("2 - Fazer PIX")
        print("3 - Adicionar saldo")
        print("4 - Ver extrato")
        print("5 - Somar pix enviados")
        print("6 - Sair")

        opcao = input("Selecione uma das opções: ")

        if opcao == "1":
            conta.mostrar_saldo()
            
        elif opcao == "2":
            conta.fazer_pix()
            
        elif opcao == "3":
            conta.adicionar_saldo()
            
        elif opcao == "4":
            conta.mostrar_extrato()
            
        elif opcao == "5":
            conta.somar_pix()
            
        elif opcao == "6":
            print("Encerrando o sistema!")
            break
            
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()