"""
Este código é o contrato da classe UsuarioComum
Aqui se determina os atributos e métodos obrigatórios
"""
#colocar os tipos livro e pessoa nos metodos, herdar ambas


from src.models.pessoa_cnt import Pessoa
from abc import ABC, abstractmethod

class UsuarioComum_cnt(Pessoa):
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
    def contar_leitura(self,paginas: int, tempo: float)-> None:
        """
        Registra páginas e o tempo de leitura
        """
        pass

    @abstractmethod
    def seguir_pessoa(self, usuario)-> None:
        """
        Adiciona uma pessoa à lista de amigos
        """
        pass
    @abstractmethod
    def cadastrar_livro(self, livro, bd)-> bool:
        """
        Cadastra um livro exixtente no banco de dados
        na biblioteca pessoal
        Retorno será True caso o cadastro seja realizado e False
        se não for concluído
        """
        pass

    @abstractmethod
    def adicionar_lista_desejo(self, livro)-> None:#ou bool pra verificar, nn?
        """
        Adiciona um livro à lista de desejos
        """
        pass

    @abstractmethod
    def avaliar_livro(self, livro, nota, resenha)-> None:
        """
        Registra nota e/ou resenha de um livro
        """
        pass

    @abstractmethod
    def registrar_trecho(self, livro, trecho)-> None:
        """
        Registra um trecho interessante de um livro
        """
        pass



#esperar metodos de pessoa

