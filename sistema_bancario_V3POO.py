from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transação(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou. Saldo insuficiente.")

        elif valor > 0:
            print("Saque realizado com sucesso!")
            return True

        else:
            print("Operação falhou. Numero informado invalido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso!")

        else:
            print("Operação falhou. Valor informado invalido")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = "500", limite_saque = "3"):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def Sacar(self, valor):
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque > self.limite_saque

        if excedeu_limite:
            print("Operação falhou. Valor acima do limite permitido.")

        elif excedeu_saques:
            print("Operação falhou. Limite de saque atingido")

        else:
            super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
                Agencia: {self.agencia}
                C/C: {self.conta}
                Titular: {self.cliente.nome}
                """


class Historico:
    def __init__(self,transacoes):
        self._transacoes = []

    @property
    def trasacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
        {
            "Tipo" : transacao.__class__.__name__,
            "Valor": transacao.valor,
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(valor):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class sacar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Menu():
    def __init__(self,titulo, opcoes):
        self.titulo = titulo
        self.opcao = opcoes

    def exibir(self):
        print(f"\n{'-' * 44}\n  \t\t{self.titulo}\n{'-' * 44}")
        for numero, opcoes in enumerate(self.opcao, start=1):
            print(f"{numero} - {opcoes}")

def filtrar_clientes(clientes, cpf):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes):
    cpf = input("Digite o CPF (somente números): ")
    cliente = filtrar_clientes(clientes, cpf)
    if cliente:
        print("CPF ja cadastrado!")
        return
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

def criar_conta(clientes_filtrados, contas, clientes, agencia, numero):

    cpf = input("Digite seu cpf: ")

    if clientes_filtrados == cpf:
        conta = {
            "agencia": agencia,
            "conta": numero,
            "nome": clientes_filtrados,
        }

        contas.append(conta)
        print("Conta criada com sucesso.")

def main():
    clientes = []
    contas = []

    menu_principal = Menu(
        "SUPER BANK",
        [
            "Sacar",
            "Depositar",
            "Extrato",
            "Novo Usuário",
            "Criar conta",
            "Listar contas",
            "Sair",
        ],
    )

    while True:
        menu_principal.exibir()

        escolha = input("Digite o número da opção:")

        if escolha == "1":
            sacar(clientes)

        elif escolha == "2":
            pass

        elif escolha == "3":
            pass

        elif escolha == "4":
            criar_cliente(clientes)

        elif escolha == "5":
            criar_conta()

        elif escolha == "6":
            print(clientes)

        elif escolha == "7":
            break

        else:
            print("\nOpção inválida, tente novamente!")

main()

