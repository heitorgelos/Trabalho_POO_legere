"""
Este código é o contrato da classe Usuario
Aqui se determina os atributos e métodos obrigatórios
"""
from src.models.BDManager_cnt import BDManager_cnt
from src.models.livro_cnt import Livro_cnt
from abc import ABC, abstractmethod

class Usuario_cnt(ABC):

    @abstractmethod
    def resumo_desempenho(self) -> None:
        """
        Exibe um resumo estatístico do usuário
        """
        pass

    @abstractmethod
    def construtor_bd(self, solicitante: BDManager_cnt, dados: dict) -> None:
        """
        Construtor utilizado pelo banco de dados
        """
        pass

    @abstractmethod
    def consultar_perfil(self) -> None:
        """
        Exibe informações do perfil de acordo com o tipo de usuário
        """
        pass

    @abstractmethod
    def ver_amigos(self)-> list:
        """
        Retona a lista de amizades do usuário
        """
        pass

    @abstractmethod
    def definir_meta(self)-> None:
        """
        Registra metas como quantidade de páginas ou de livros
        """
        pass

    @abstractmethod
    def consultar_metas_progresso(self)-> None:
        """
        Exibe metas cadastradas pelo usuário e o seu progresso
        """
        pass

    @abstractmethod
    def registrar_tempo_leitura(self, tempo: float, data: str)-> None:
        """
        Registro de duas formas: acumulativa de todos os dias de uso e quanto leu por dia
        """ 
        pass

    @abstractmethod
    def registrar_paginas_lidas(self, valor:int)-> None:
        """
        Registra de maneira acumulativa a quantidade de páginas lidas
        """
        pass

    @abstractmethod
    def registrar_paginas_por_mes(self, mes: str, paginaslidas: int)-> None:
        """
        Registra a quantidade de páginas lidas em um mês
        """
        pass

    @abstractmethod
    def seguir_pessoa(self, usuario: 'Usuario')-> None:
        """
        Adiciona uma pessoa à lista de amigos
        """
        pass

    @abstractmethod
    def cadastrar_livro_bp(self, livro:Livro_cnt, bd:BDManager_cnt)-> None:
        """
        Cadastra um livro exixtente no banco de dados na biblioteca pessoal
        """
        pass

    @abstractmethod
    def adicionar_lista_desejo(self, livro: Livro_cnt, bd: BDManager_cnt)-> None:
        """
        Adiciona um livro à lista de desejos
        """
        pass

    @abstractmethod
    def remover_lista_desejo(self, livro: Livro_cnt, bd: BDManager_cnt)->None:
        """
        Remove um livro da lista de desejo
        """
        pass

    @abstractmethod
    def avaliar_livro(self, livro: Livro_cnt, nota: float, resenha: str)-> None:
        """
        Registra nota e resenha de um livro
        """
        pass

    @abstractmethod
    def registrar_trecho(self, livro: Livro_cnt, trecho:str)-> None:
        """
        Registra um trecho interessante de um livro
        """
        pass
    
    @abstractmethod
    def iniciar_leitura(self, livro: Livro_cnt, bd:BDManager_cnt)-> None:
        """
        Define o livro atual do usuário
        """
        pass

    @abstractmethod
    def concluir_leitura(self)-> None:
        """
        Registra a conclusão do livro que estava sendo lido
        """
        pass

    @abstractmethod
    def abandonar_leitura(self)-> None:
        """
        Registra o abandono de um livro
        """
        pass

    @abstractmethod
    def adicionar_preferencia(self,genero: str)-> None:
        """
        Adiciona um gênero literário às preferências do usuário
        """
        pass

    @abstractmethod
    def remover_preferencia(self,genero: str)-> None:
        """
        Remove um gênero literário das preferências do usuário
        """
        pass

    @abstractmethod
    def consultar_preferencia(self)-> list:
        """
        Retorna os gêneros literários cadastrados nas preferências do usuário
        """
        pass



    


