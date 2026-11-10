"""
Este código é o contrato da classe BDmanager.
Aqui se determina os atributos e métodos obrigatórios
"""
from abc import ABC, abstractmethod

class BDManager_cnt(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def carregar_database(self) -> bool:
        """
        Carrega as bases de dados externas de livros e usuários 
        """
        pass

    @abstractmethod
    def validar_objeto(self, obj) -> tuple[bool, any]:
        """
        Recebe um objeto e pesquisa se ele de fato existe na base de dados, se sim retorna true se não retorna False
        Para usuários: busca pelo nome e login -> inalteráveis
        Para livros: busca pelo título -> inalteráveis
        """
        pass

    @abstractmethod
    def atualizar_objeto(self, obj_original) -> bool:
        """
        Atualiza a base de dados com as novas informações 
        Para usuários: busca pelo nome e login -> inalteráveis
        Para livros: busca pelo título -> inalteráveis
        """
        pass 


   