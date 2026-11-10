"""
Este código é o contrato da classe Livro
Aqui se determina os atributos e métodos obrigatórios
"""

from abc import ABC, abstractmethod

class Livro_cnt(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def avaliar(nota: float, resenha: str) -> None:
        """
        Permite avaliar um livro ( Resenha e Nota )
        """
        pass
