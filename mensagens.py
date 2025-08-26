import os


class Mensagens:
    ICONES = {
        "ERRO": "❌",
        "SUCESSO": "✅",
        "INFO": "ℹ️",
        "EXTRATO": "📄",
        "AVISO": "⚠️",
    }

    @staticmethod
    def exibir(texto, titulo="INFO"):   # EXIBE MENSAGENS NA TELA
        largura = 50
        icone = Mensagens.ICONES.get(titulo.upper(), "")
        print("\n" + "=" * largura)
        print(f"{icone}  {titulo.center(largura - 8)}  {icone}")
        print("-" * largura)

        # centraliza o bloco principal
        print(texto.center(largura))
        print("=" * largura + "\n")

    @staticmethod                       # FAZ A TELA PAUSAR ANTES DE LIMPAR
    def pausar(msg="\nAperte Enter para continuar..."):
        input(msg)

    @staticmethod
    def limpar_tela():                  #DEIXA A TELA DO TERMINAL LIMPA
        os.system("cls" if os.name == "nt" else "clear")




