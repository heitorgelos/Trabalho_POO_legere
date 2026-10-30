"""
Este código é a implementação da classe UsuarioComum
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.usuario_comum_cnt import UsuarioComum_cnt
#from src.implement.BDManager_imp import BDmanager
from src.implement.Livro_imp import Livro


class UsuarioComum(UsuarioComum_cnt):
    def __init__(self, nome, login, senha):
        super().__init__(nome, login, senha)
        self.__biblioteca_pessoal = []
        self.__biblioteca_desejo = []
        self.__livro_atual = None
        self.__livros_lidos = []
        self.__paginometro = 0
        #self.__tempo_medio_leitura = 0.0
        self.__tempo_de_leitura = 0.0
        self.__preferencias_genero = []
        self.__livros_abandonados = []
        self.__amigos = []
        self.__trechos_pref = []
        self.__meta_paginas_dia = 0
        self.__meta_livros_mes = 0
        self.__xp = 0
        self.__ofensiva = 0

    def resumo_desempenho(self):
        qntd_livro = len(self.__livros_lidos)
        print(f"Quantidade de livros lidos: {qntd_livro}")
        print(f"Paginômetro: {self.__paginometro}")
        print(f"Pontos de XP: {self.__xp}")
        print(f"Dias de ofensiva: {self.__ofensiva}")

    def ver_amigo(self):
        return self.__amigos

    def definir_meta(self):
        meta = input("Prefere definir uma meta de paginas ou livros?")
        if meta == "paginas":
            qntd_paginas = int(input("Quantas paginas por dia?"))
            self.__meta_paginas_dia = qntd_paginas
        elif meta == "livros":
            qntd_livros = int(input("Quantos livros por mês?"))
            self.__meta_livros_mes = qntd_livros

    def contar_leitura(self, paginas: int, tempo: float):
        self.__paginometro += paginas
        self.__tempo_de_leitura += tempo

    def seguir_pessoa(self, user):
        if isinstance(user, UsuarioComum):
            self.__amigos.append(user)

        else:
            raise ValueError("É possível seguir apenas usuários cadastrados")

    def cadastrar_livro(self, livro, bd):
        #esperar as duas classes para utilizar metodos de busca
        pass

    def adicionar_lista_desejo(self, livro):
        #fazer verificação se existe no bd
        if isinstance(livro, Livro):
            self.__biblioteca_desejo.append(livro)
        else:
            raise ValueError("Apenas livros podem ser adicionados à lista de desejos")

    def avaliar_livro(self, livro, nota, resenha):
        #esperadno classe livro pra saber como nota e resenha serao armazenadas
        pass

    def registrar_trecho(self, livro, trecho):
        if isinstance(livro, Livro):
            registro = {"livro": livro, "texto": trecho}
            self.__trechos_pref.append(registro)
        else:
            raise ValueError("Só é possível registrar trechos de livros")











