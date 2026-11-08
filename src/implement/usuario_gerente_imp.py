from src.implement.usuario_imp import Usuario
from src.implement.livro_imp import Livro
from src.implement.clube_livro_imp import ClubeLivro
from src.implement.usuario_comum_imp import UsuarioComum


class UsuarioGerente(Usuario):
    def __init__(self, nome, login, senha)->None:
        super().__init__(nome, login, senha)
        self._permissao_gerenciar = True


    def consultar_perfil(self)->None:
        print(f"Nome: {self._nome}")
        print(f"Login: {self._login}")
        print("Tipo de conta: Gerente")

    def criar_clube(self)->ClubeLivro:
        clube = ClubeLivro(self)
        return clube

    def adicionar_participante(self, clube: ClubeLivro, user: UsuarioComum):
        clube.adicionar_pessoa(self, user)

    def remover_participante(self, clube: ClubeLivro, user: UsuarioComum)->None:
        clube.expulsar_pessoa(self, user)
        
    def adicionar_livro(self, clube: ClubeLivro, livro: Livro)->None:
        clube.adicionar_livro(self, livro)

    #def excluir_clube(self, clube: Clube)
    #adicionar masi metodos pra mexer em Clube

    
