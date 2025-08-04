
### SISTEMA BANCARIO  ###

#VARIAVEIS

limite_saque = 500
limite_diario = 3
saldo = 0
extrato_bancario = []

#Função MENU

def menu():
    menu = """
  --------------------
  | CAIXA ELETRONICO |
  --------------------

    1 - Sacar
    2 - Depositar
    3 - Extrato
    4 - Sair
    """
    print(menu.center(5))
    escolha = input("Escolha uma opção:")

    return escolha

#Função de SACAR
def sacar(saldo, limite_diario, extrato_bancario):
    print("\n===========  Sacar  ===========")
    print(f"Limite por saque: R${limite_saque:.2f}")
    print(f"Limite diario: {limite_diario}")

    if saldo == 0:
        print("\nSem saldo em conta.")
        return saldo, limite_diario, extrato_bancario
    elif limite_diario == 0:
        print("\nLimite diario atingido.")
        return saldo, limite_diario, extrato_bancario

    while True:
        try:
            saque_feito = float(input("\nDigite o valor que deseja sacar: R$"))
            if saque_feito > saldo:
                print("Saldo insuficiente!")
                break
            else:
                saldo -= saque_feito
                limite_diario -= 1
                extrato_bancario.append(f"Saque:    R${saque_feito:.2f}")
                print("Saque realizado com sucesso!")
                break
        except ValueError:
            print("Valor invalido, digite um número")
    return saldo, limite_diario, extrato_bancario

#Função de DEPOSITO
def depositar(saldo, extrato_bancario, /):
    while True:
        try:
            deposito = float(input("Valor de deposito: R$"))
            if deposito < 0:
                print("Valor inválido, valor não pode ser abaixo de Zero!")
                return saldo, extrato_bancario
            else:
                saldo += deposito
                print("Deposito realizado com sucesso!")
                extrato_bancario.append(f"Deposito: R${deposito:.2f}")
                break
        except ValueError:
            print("Valor inválido, digite um número!")
    return saldo, extrato_bancario

#Função de EXTRATO
def extrato(saldo, extrato_bancario):
    print("\n==========  Extrato  ==========")
    if not extrato_bancario:
        print("Nenhum deposito realizado.")
        print(f"\nSaldo:    R${saldo:.2f}")
        print("===============================")
    else:
        for movimento in extrato_bancario:
            print(movimento)
        print(f"\nSaldo:    R${saldo:.2f}")
        print("===============================")

#LOOP PRINCIPAL
while True:
    escolha = menu()

    if escolha == "1":
        saldo, limite_diario, extrato_bancario = sacar(saldo, limite_diario, extrato_bancario)

    elif escolha == "2":
        saldo, extrato_bancario = depositar( saldo, extrato_bancario)

    elif escolha == "3":
        extrato(saldo, extrato_bancario)

    elif escolha == "4":
        break

    else:
        print("\nOpção inválida, tente novamente!")