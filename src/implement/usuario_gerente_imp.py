from src.implement.usuario_imp import Usuario
#from src.implement.BDManager_imp import BDmanager
#from src.implement.livro_imp import Livro

class UsuarioGerente(Usuario):
    def __init__(self, nome, login, senha):
        super().__init__(nome, login, senha)
        self._permissao_gerenciar = True

    def consultar_perfil(self)->None:
        print(f"Nome: {self._nome}")
        print(f"Login: {self._login}")
        print("Tipo de conta: Gerente")
 
    #def remover_participante(self, clube: Clube user: UsuarioComum)
    #def adicionar_participante(self, clube: Clube, user: UsuarioComum)
    #def criar_clube(self, nome: str)
    #def excluir_clube(self, clube: Clube)
    #adicionar masi metodos pra mexer em Clube

    
