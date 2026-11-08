"""
Este código é o contrato da classe UsuarioComum
Aqui se determina os atributos e métodos obrigatórios
"""

#from src.models.pessoa_cnt import Pessoa
from src.models.BDManager_cnt import BDManager_cnt
from src.implement.livro_imp import Livro
from abc import ABC, abstractmethod

class UsuarioComum_cnt():
    def __init__(self, nome, login, senha):
        super().__init__(nome, login, senha)

    @abstractmethod
    def resumo_desempenho(self) -> None:
        """
        Exibe um resumo estatístico do usuário
        """
        pass

    @abstractmethod
    def ver_amigo(self)-> list:
        """
        Exibe a lista de amizades do usuário
        """
        pass

    @abstractmethod
    def definir_meta(self)-> None:
        """
        Registra metas como quantidade de páginas ou de livros
        """
        pass

    @abstractmethod
    def consultar_meta(self)-> None:
        pass

    @abstractmethod
    def registrar_tempo_leitura(self, tempo: float)-> None:
        pass

    @abstractmethod
    def registrar_paginas_lidas(self, valor:int)-> None:
        pass

    @abstractmethod
    def registrar_paginas_por_mes(self, mes: str, paginaslidas: int)-> None:
        pass

    @abstractmethod
    def seguir_pessoa(self, usuario)-> None:
        """
        Adiciona uma pessoa à lista de amigos
        """
        pass
    @abstractmethod
    def cadastrar_livro_bp(self, livro, bd)-> bool:
        """
        Cadastra um livro exixtente no banco de dados
        na biblioteca pessoal
        Retorno será True caso o cadastro seja realizado e False
        se não for concluído
        """
        pass

    @abstractmethod
    def adicionar_lista_desejo(self, livro: Livro, bd: BDmanager)-> None:#ou bool pra verificar, nn?
        """
        Adiciona um livro à lista de desejos
        """
        pass

    @abstractmethod
    def avaliar_livro(self, livro: Livro, nota: float, resenha: str)-> None:
        """
        Registra nota e/ou resenha de um livro
        """
        pass

    @abstractmethod
    def registrar_trecho(self, livro: Livro, trecho:str)-> None:
        """
        Registra um trecho interessante de um livro
        """
        pass
    @abstractmethod
    def iniciar_leitura(self, livro: Livro)-> None:
        pass

    @abstractmethod
    def concluir_leitura(self)-> None:
        pass

    @abstractmethod
    def bandonar_leitura(self)-> None:
        pass

    @abstractmethod
    def adicionar_preferencia(self,genero: str)-> None:
        pass

    @abstractmethod
    def remover_preferencia(self,genero: str)-> None:
        pass

    @abstractmethod
    def consultar_preferencia(self,genero: str)-> None:
        pass

#esperar metodos de pessoa

