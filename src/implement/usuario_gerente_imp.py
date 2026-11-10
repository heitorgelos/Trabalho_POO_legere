from src.implement.usuario_imp import Usuario
from src.implement.livro_imp import Livro
from src.models.clube_livro_cnt import ClubeLivro_cnt
#from src.implement.clube_livro_imp import ClubeLivro
from src.implement.usuario_comum_imp import UsuarioComum


class UsuarioGerente(Usuario):
    def __init__(self, nome, login, senha)->None:
        super().__init__(nome, login, senha)
        self.__clube = None


    def consultar_perfil(self)->None:
        print(f"Nome: {self._nome}")
        print(f"Login: {self._login}")
        print("Tipo de conta: Gerente")

    @property
    def clube(self):
        return self.__clube

    def criar_clube(self)-> 'ClubeLivro':
        from src.implement.clube_livro_imp import ClubeLivro

        if self.__clube is not None:
            raise ValueError("Você já possui um clube")
        
        self.__clube = ClubeLivro(self)
        return self.__clube

    def nomear_clube(self, clube:ClubeLivro_cnt, nome: str) -> bool:
        clube.definir_nome(self,nome)

    def passar_moderacao(self, clube, novo_moderador) -> bool:
        clube.redefinir_moderador(self, novo_moderador)
        
    def ver_expulsos(self, clube) -> list:
        return clube.ver_expulsos(self)

    def adicionar_participante(self, clube: ClubeLivro_cnt, user: UsuarioComum) -> bool:
        clube.adicionar_pessoa(self, user)

    def remover_participante(self, clube: ClubeLivro_cnt, user: UsuarioComum) -> bool:
        clube.expulsar_pessoa(self, user)
        
    def adicionar_livro(self, clube: ClubeLivro_cnt, livro: Livro) -> bool:
        clube.adicionar_livro(self, livro)

    def deletar_clube(self, clube: ClubeLivro_cnt) -> bool:
        if self.__clube == clube:
            clube.limpar_clube(self)
            self.__clube = None

        else:
            raise ValueError("Você não possui nenhum clube cadastrado")



    


    
