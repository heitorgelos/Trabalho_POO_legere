"""
Este código é a implementação da classe UsuarioComum
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.usuario_comum_cnt import UsuarioComum_cnt
from src.models.BDManager_cnt import BDManager_cnt
from src.implement.livro_imp import Livro


class UsuarioComum(UsuarioComum_cnt):
    def __init__(self, nome, login, senha):
        #super().__init__(nome, login, senha)
        self.nome = nome
        self.login = login
        self.senha = senha
        self.__biblioteca_pessoal = []
        self.__biblioteca_desejo = []
        self.__livro_atual = None
        self.__livros_lidos = []
        self.__paginometro = {}
        self.__paginas_lidas_totais = 0
        self.__tempo_medio_leitura_min_dia = 0.0 # já vem informação no construtor
        self.__tempo_de_leitura_total = 0.0
        self.__preferencias_genero = []
        self.__livros_abandonados = []
        self.__amigos = []
        self.__trechos_pref = []
        self.__metas_leitura = []
        self.__xp = 0
        self.__ofensiva = 0

    def resumo_desempenho(self):
        qntd_livro = len(self.__livros_lidos)
        print(f"Quantidade de livros lidos: {qntd_livro}")
        print(f"Pontos de XP: {self.__xp}")
        print(f"Dias de ofensiva: {self.__ofensiva}")
        print(f"Tempo total de leitura: {self.__tempo_de_leitura_total} h")

    def ver_amigo(self):
        return self.__amigos

    def definir_meta(self):
        meta = input("Prefere definir uma meta de páginas ou livros?")
        #normalização de entradas
         #converte para letras minúsculas:
        meta = meta.lower() #ver sobre unicode e separação de acentos

        if meta == "paginas" or "páginas":
            alvo = int(input("Quantas paginas por mês?"))
            nova_meta = {"tipo": "paginas_por_mes", "alvo": alvo}
            self.__metas_leitura.append(nova_meta)
        if meta == "livros":
            alvo = int(input("Quantos livros por ano?"))
            nova_meta = {"tipo": "livros_por_ano", "alvo": alvo}
            self.__metas_leitura.append(nova_meta)
        else:
            raise ValueError("Meta inválida")

    def consultar_metas(self):
        if not self.__metas_leitura:
            print("Você não possui metas cadastradas")

        else:
            for meta in self.__metas_leitura:#percorre uma lista e em cada posição printa o dict
                print(f"Tipo:{meta['tipo']}")
                print(f"Alvo:{meta['alvo']}")

    def registrar_tempo_leitura(self, tempo: float):
        if tempo < 0:
            raise ValueError("Tempo deve ser positivo")
        if not isinstance(tempo, (float,int)):
            raise TypeError("O tempo deve ser escrito numericamente")
        else:
            self.__tempo_de_leitura_total += tempo

    def registrar_paginas_lidas(self, valor: int):
        if valor < 0:
            raise ValueError("Números de páginas deve ser positivo")
        if not isinstance(valor,int):
            raise TypeError("A quantidade de páginas lidas deve ser um número inteiro")
        else:
            self.__paginas_lidas_totais += valor

    def registrar_paginas_por_mes(self, mes: str, paginaslidas: int):
        if paginaslidas < 0:
            raise ValueError("Números de páginas lidas deve ser positivo")
        if not isinstance(mes, str):
            raise TypeError("O mês deve ser escrito por extenso")
        #verificação do mes: lista com nomes abreviados(ver)
        else:
            self.__paginometro[mes] = paginaslidas 

    def seguir_pessoa(self, user:UsuarioComum):
        if user is self:
            raise ValueError("Um usuário não pode seguir a si mesmo")
        
        elif not isinstance(user, UsuarioComum):#ver melhor esse aviso aq
            raise ValueError("É possível seguir apenas usuários cadastrados")
        
        elif user in self.__amigos:
            raise ValueError("Você já segue esse usuário")

        else:
            self.__amigos.append(user)

    def cadastrar_livro_bp(self, livro:Livro, bd:BDmanager):
        if bd.validar_objeto(livro) == False:
            raise ValueError("Este livro não existe no banco de dados")
        else:
            self.__biblioteca_pessoal.append(livro)
            print(f"Agora o livro{livro.titulo} está cadastrado na sua biblioteca pessoal")

    def adicionar_lista_desejo(self, livro: Livro, bd: BDmanager):#fazer verificação se é obj ou nn??
        if bd.validar_objeto(livro) == False:
            raise ValueError("Livro não consta no banco de dados")
        else:
            self.__biblioteca_desejo.append(livro)

    def avaliar_livro(self, livro: Livro, nota: float, resenha: str):
        #verificar a versao final do metodo
        livro.avaliar(nota, resenha)

    def registrar_trecho(self, livro: Livro, trecho: str):
        if isinstance(livro, Livro):
            registro = {"livro": livro, "texto": trecho}
            self.__trechos_pref.append(registro)  #os trechos pref são informações dadas pelo usuário e cada resgistro liga o trecho a um livro referente
        else:
            raise ValueError("Só é possível registrar trechos de livros")

    def iniciar_leitura(self, livro: Livro):#seria bom ver a existênciano bd?
        if not  isinstance(livro, Livro):
            raise ValueError("Livro inválido")
        self.__livro_atual = livro

    def concluir_leitura(self):
        livroconcluido = self.__livro_atual
        self.__livros_lidos.append(livroconcluido)
        self.__livro_atual = None

    def abadonar_leitura(self):
        livroabandonado = self.__livro_atual
        self.__livros_abandonados.append(livroabandonado)
        self.__livro_atual = None

    def adicionar_preferencia(self, genero:str):
        if not isinstance(genero, str):
            raise TypeError("O gênero deve ser escrito")
        genero_format = genero.strip()
        if not genero_format:
            raise ValueError("Gênero não pode ser vazio")
        
        self.__preferencias_genero.append(genero_format)
      
    def remover_preferencia(self, genero:str):#list comprehension: evita bugs e é mais rápida que o for tradicional
        self.__preferencias_genero =[gen for gen in self.__preferencias_genero if gen != genero]

    def consultar_preferencia(self):
        return self.__preferencias_genero











