import os
import textwrap


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input('\nAperte enter para continuar!')

def menu():
    limpar_tela()
    menu = """
  ----------------------
  |     SUPER BANK     |
  ----------------------

    1 - Sacar
    2 - Depositar
    3 - Extrato
    4 - Novo Usuário
    5 - Criar conta
    6 - Listar contas
    7 - Sair
    """
    print(textwrap.dedent(menu))
    escolha = input("Escolha uma opção:")

    return escolha

def cadastro_usuario(users):
    print("\n------------ Verificação -------------")
    cpf = input("CPF:")
    if cpf.isdigit():
        for user in users:
            if user["cpf"] == cpf:
                print("Error! CPF já cadastrado.")
                pausar()
                return

        print("\n============= Cadastro ==============")
        nome = input("Nome completo:")
        nascimento = input("Data de nascimento (dd-mm-aa):")
        endereco = input("Endereço (Logradoro, Número - Bairro - Cidade/Estado):")

        #VALIDAR CAMPOS OBRIGATORIOS
        if not cpf or not nome or not nascimento or not endereco:
            print("Error. Todos os campos são obrigatorios")
            pausar()
            return

        usuario = {
        "cpf": cpf,
        "nome": nome,
        "nascimento": nascimento,
        "endereco": endereco,
        }
        users.append(usuario)
        print("\nUsuario cadastrado com sucesso.")
        pausar()
    else:
        print("Entrada invalida. Apenas números.")
        pausar()

def criar_conta(AGENCIA, numero_conta, contas, users):
    conta = input("\nDigite seu CPF:")
    for user in users:
        if user["cpf"] == conta:
            conta = {
            "agencia":AGENCIA,
            "conta":numero_conta,
            "nome":user['nome'],
            }

            contas.append(conta)
            print("Conta criada com sucesso.")
            pausar()
            return int(numero_conta) + 1
    print("Usuário não encontrato. Cadastre-se primeiro")
    pausar()
    return numero_conta

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        pausar()
        return
    else:
        for conta in contas:
            menu =f"""
                Agencia:\t{conta["agencia"]}
                C/C: \t\t{conta["conta"]}
                Titular: \t{conta["nome"]}
            """
            print(textwrap.dedent(menu))
    pausar()

def sacar(saldo, limite_diario, extrato_bancario):
    limite_saque = 500

    print("\n===========  Sacar  ===========")
    print(f"Limite por saque: \tR${limite_saque:.2f}")
    print(f"Limite diario: \t\t{limite_diario}")

    if saldo == 0:
        print("\nSem saldo em conta.")
        pausar()
        return saldo, limite_diario, extrato_bancario
    elif limite_diario == 0:
        print("\nLimite diario atingido.")
        pausar()
        return saldo,limite_diario, extrato_bancario

    while True:
        try:
            saque_feito = float(input("\nDigite o valor que deseja sacar: R$"))
            if saque_feito > saldo:
                print("Saldo insuficiente!")
                pausar()
                break
            elif saque_feito > limite_saque:
                print("Valor acima do limite permitido.")
                pausar()
            else:
                saldo -= saque_feito
                limite_diario -= 1
                extrato_bancario.append(f"Saque:\t\tR${saque_feito:.2f}")
                print("Saque realizado com sucesso!")
                pausar()
                break
        except ValueError:
            print("Valor invalido, digite um número")
            pausar()
    return saldo, limite_diario, extrato_bancario

def depositar(saldo:float, extrato_bancario, /):
    while True:
        try:
            deposito = float(input("Valor de deposito: R$"))
            if deposito < 0:
                print("Valor inválido, valor não pode ser abaixo de Zero!")
                pausar()
                return saldo, extrato_bancario
            else:
                saldo += deposito
                print("Deposito realizado com sucesso!")
                extrato_bancario.append(f"Deposito: \tR${deposito:.2f}")
                pausar()
                break
        except ValueError:
            print("Valor inválido, digite um número!")
            pausar()
    return saldo, extrato_bancario

def extrato(saldo,/,*, extrato_bancario):
    print("\n==========  Extrato  ==========")
    if not extrato_bancario:
        print("Nenhum deposito realizado.")
        print(f"\nSaldo: \tR${saldo:.2f}")
        print("===============================")
        pausar()
    else:
        for movimento in extrato_bancario:
            print(movimento)
        print(f"\nSaldo: \t\tR${saldo:.2f}")
        print("===============================")
        pausar()

def main():
    AGENCIA = "0001"
    numero_conta = 1
    users = []
    contas = []

    saldo = 0
    limite_diario = 3
    extrato_bancario = []

    while True:
        escolha = menu()

        if escolha == "1":
            saldo, limite_diario, extrato_bancario = sacar(saldo, limite_diario, extrato_bancario)

        elif escolha == "2":
            saldo, extrato_bancario = depositar(saldo, extrato_bancario)

        elif escolha == "3":
            extrato(saldo, extrato_bancario = extrato_bancario)

        elif escolha == "4":
            cadastro_usuario(users)

        elif escolha == "5":
            numero_conta = criar_conta(AGENCIA, numero_conta, contas, users)

        elif escolha == "6":
            listar_contas(contas)

        elif escolha == "7":
            break

        else:
            print("\nOpção inválida, tente novamente!")

main()