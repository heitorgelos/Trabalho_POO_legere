"""
Este código é o contrato da classe BDmanager.
Aqui se determina os atributos e métodos obrigatórios
"""
from abc import ABC, abstractmethod

class ClubeLivro_cnt(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def carregar_dados(self):
        """
        Carrega os livros da base de dados
        """
        pass

    @abstractmethod
    def salvar_dados(self):
        """
        Salva os dados de pessoas do clube, expulsos e livros na base de dados
        """
        pass
    
    @abstractmethod
    def adicionar_livro(self):
        """
        Somente acessível ao moderador
        Adiciona livro na lista de livros
        """
        pass

    @abstractmethod
    def adicionar_pessoa(self):
        """
        Somente acessível ao moderador
        Adiciona uma pessoa no clube verificando se o limite de integrantes não foi
        ultrapassado e se a pessoa não foi banida anteriormente. 
        Salva os nomes dos integrantes em um arquivo
        """
        pass

    @abstractmethod
    def expulsar_pessoa(self):
        """
        Somente acessível ao moderador
        Expulsa uma pessoa do clube, salvando seu nome no arquivo de banidos
        """
        pass

    @abstractmethod
    def redefinir_moderador(self): 
        """
        Redefine quem é o administrador do clube, somente pode ser feito pelo atual moderador
        """
        pass 
   