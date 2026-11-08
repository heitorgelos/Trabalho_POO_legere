from src.implement.usuario_imp import Usuario
from src.implement.livro_imp import Livro
from src.models.clube_livro_cnt import ClubeLivro_cnt
from src.implement.usuario_comum_imp import UsuarioComum


class UsuarioGerente(Usuario):
    def __init__(self, nome, login, senha)->None:
        super().__init__(nome, login, senha)
        self._permissao_gerenciar = True


    def consultar_perfil(self)->None:
        print(f"Nome: {self._nome}")
        print(f"Login: {self._login}")
        print("Tipo de conta: Gerente")

    def criar_clube(self)->ClubeLivro_cnt:
        clube = ClubeLivro_cnt(self)
        return clube

    def adicionar_participante(self, clube: ClubeLivro_cnt, user: UsuarioComum):
        clube.adicionar_pessoa(self, user)

    def remover_participante(self, clube: ClubeLivro_cnt, user: UsuarioComum)->None:
        clube.expulsar_pessoa(self, user)
        
    def adicionar_livro(self, clube: ClubeLivro_cnt, livro: Livro)->None:
        clube.adicionar_livro(self, livro)

    #def excluir_clube(self, clube: Clube)
    #adicionar masi metodos pra mexer em Clube

    
