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
        Recebe um objeto e pesquisa se ele de fato existe na base de dados, se sim retorna ele
        se não retorna None
        """
        pass

