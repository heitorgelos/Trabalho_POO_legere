"""
Este código é o contrato da classe BDmanager.
Aqui se determina os atributos e métodos obrigatórios
"""
from abc import ABC, abstractmethod

class BDManager_cnt(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def carregar_database(self):
        """
        Carrega as bases de dados externas de livros e usuários 
        """
        pass

    @abstractmethod
    def validar_objeto(self):
        """
        Recebe um objeto e pesquisa se ele de fato existe na base de dados, se sim retorna true se não retorna False
        """
        pass

    @abstractmethod
    def indicar_objeto(self):
        """
        Usará IA para indicar um livro ou objeto de possível agrado do usuário de acordo com suas preferências
        """


    @abstractmethod
    def atualizar_objeto(self, obj): 
        """
        Atualiza a base de dados com as novas informações 
        """
        pass 
   