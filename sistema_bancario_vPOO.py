from abc import ABC, abstractclassmethod, abstractproperty
from mensagens import Mensagens

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
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
            self._saldo -= valor
            return True

        else:
            print("Operação falhou, Numero informado invalido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
        else:
            print("Operação falhou, Valor informado invalido!")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len([transacao for transacao in self.historico.
        transacoes if transacao["tipo"] == Saque.
        __name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque >= self.limite_saque

        if excedeu_limite:
            Mensagens.exibir("Valor acima do limite permitido de R$500", titulo="ERRO")
            return False

        if excedeu_saque:
            Mensagens.exibir("Limite de saque diario atingido", titulo= "ERRO")
            return False

        super().sacar(valor)
        Mensagens.exibir(f"Saque de R${valor:.2f} realizado!", titulo="SUCESSO")
        return True


    def __str__(self):
        return f"""\
                Agencia: {self.agencia}
                C/C: {self.numero}
                Títular: {self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
        {

            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(valor):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
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


class Menu:
    def __init__(self, titulo, subtitulo, opcoes):
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.opcaos = opcoes

    menu_principal = (
        "SUPER BANK",
        "Menu Principal",
        [
            "Sacar",
            "Depositar",
            "Extrato",
            "Novo cliente",
            "Criar conta",
            "Listar clientes",
            "Listar contas",
            "Sair",
        ],
    )

    def exibir(self, largura=50):
        print("=" * largura)
        print(self.titulo.center(largura))
        print("=" * largura)
        print(self.subtitulo.center(largura))
        print("-" * largura)

        for numero, opcoes in enumerate(self.opcaos, start=1):
            print(f"{numero:>2} - {opcoes}")
        print("=" * largura)


class BancoGeral:            #CLASSE UTILITARIA
    @staticmethod
    def filtrar_clientes(clientes, cpf):
        clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    @staticmethod
    def criar_clientes(clientes):
        cpf = input("\nDigite o CPF: ")
        cliente = BancoGeral.filtrar_clientes(clientes, cpf)

        if cliente:
            Mensagens.exibir("CPF ja cadastrado!", titulo="AVISO")
            return

        nome = input("Nome completo: ")
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(
            cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco
        )
        clientes.append(cliente)
        Mensagens.exibir("Cliente cadastrado com sucesso!", titulo="SUCESSO")

    @staticmethod
    def criar_contas(clientes, contas, numero_conta):
        cpf = input("\nDigite seu CPF: ")
        cliente = BancoGeral.filtrar_clientes(clientes, cpf)

        if not cliente:
            Mensagens.exibir("Cliente não encontrato.", titulo="AVISO")
            return

        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

        contas.append(conta)
        cliente.contas.append(conta)

        Mensagens.exibir("Conta criada com sucesso.", titulo="SUCESSO")

    @staticmethod
    def listar_clientes(clientes):
        for cliente in clientes:
            print(f"""
                Nome:{cliente.nome}
                CPF: {cliente.cpf}
                Data de Nascimento:{cliente.data_nascimento}
                Endereço: {cliente.endereco}
            """)

    @staticmethod
    def listar_contas(contas):
        for conta in contas:
            print("="  * 50)
            print(str(conta))

    @staticmethod
    def recuperar_conta_cliente(cliente):
        if not cliente.contas:
            return None
        #FIXME - não permite cliente escolher conta
        return cliente.contas[0]

    @staticmethod
    def depositar(clientes):
        cpf = input("\nInforme seu CPF: ")
        cliente = BancoGeral.filtrar_clientes(clientes, cpf)

        if not cliente:
            Mensagens.exibir("Cliente não encontrado!", titulo="ERRO")
            return

        conta = BancoGeral.recuperar_conta_cliente(cliente)
        if not conta:
            Mensagens.exibir("Esse CPF não possui conta!", titulo="AVISO")
            return

        valor = float(input("Valor: "))
        transacao = Deposito(valor)

        cliente.realizar_transacao(conta, transacao)
        Mensagens.exibir(f"Depósito de R${valor:.2f} realizado!", titulo="SUCESSO")

    @staticmethod
    def sacar(clientes):
        cpf = input("\nDigite seu CPF:")
        cliente = BancoGeral.filtrar_clientes(clientes, cpf)

        if not cliente:
            Mensagens.exibir("Cliente não encontrado!", titulo="ERRO")
            return

        conta = BancoGeral.recuperar_conta_cliente(cliente)

        if not conta:
            Mensagens.exibir("Esse CPF não possui conta!", titulo="AVISO")
            return

        valor = float(input("Valor:"))
        transacao = Saque(valor)

        cliente.realizar_transacao(conta, transacao)

    @staticmethod
    def extrato(clientes):
        cpf = input("Digite seu CPF: ")
        cliente = BancoGeral.filtrar_clientes(clientes, cpf)

        if not cliente:
            Mensagens.exibir("Cliente não encontrado.", titulo="ERRO")
            return

        conta = BancoGeral.recuperar_conta_cliente(cliente)

        if not conta:
            Mensagens.exibir("Esse CPF não possui conta.", titulo="AVISO")
            return

        transacoes = conta.historico.transacoes

        if not transacoes:
            Mensagens.exibir("Não houve movimentação.", titulo="AVISO")
            return

        #CABEÇALHO.
        cabecalho = (
        f"Cliente: {cliente.nome}\n"
        f"Agência: {conta.agencia} | Conta: {conta.numero}"
        ).strip()

        Mensagens.exibir(cabecalho, titulo="EXTRATO")

        for t in transacoes:
            print(f"{t['tipo']:<10} \tR${t['valor']:>10.2f}")
            # tipo à esquerda com 10 colunas; valor à direita com 10 colunas.

        print(f"\nSaldo:{'':<6} R$ {conta.saldo:>10.2f}")
        print("=" * 50 + "\n")


def main():                  #PROGRAMA PRINCIPAL
    menu = Menu(*Menu.menu_principal)
    clientes = []
    contas = []

    while True:
        #LIMPA A TELA ANTES DE MOSTRAR O MENU
        Mensagens.limpar_tela()

        #CHAMADA DO MENU
        menu.exibir()
        escolha = input("\nDigite o número da opção:")

        if escolha == "1":
            BancoGeral.sacar(clientes)
            Mensagens.pausar()

        elif escolha == "2":
            BancoGeral.depositar(clientes)
            Mensagens.pausar()

        elif escolha == "3":
            BancoGeral.extrato(clientes)
            Mensagens.pausar()

        elif escolha == "4":
            BancoGeral.criar_clientes(clientes)
            Mensagens.pausar()

        elif escolha == "5":
            BancoGeral.criar_contas(clientes, contas, len(contas) + 1)
            Mensagens.pausar()

        elif escolha == "6":
            BancoGeral.listar_clientes(clientes)
            Mensagens.pausar()

        elif escolha == "7":
            BancoGeral.listar_contas(contas)
            Mensagens.pausar()

        elif escolha == "8":
            break

        else:
            Mensagens.exibir("Entrada inválida!", titulo="ERRO")
            Mensagens.pausar()

main()