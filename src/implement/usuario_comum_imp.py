from src.implement.usuario_imp import Usuario

class UsuarioComum(Usuario):
    def __init__(self, nome, login, senha):
        super().__init__(nome, login, senha)

    def consultar_perfil(self)->None:
        print(f"Nome: {self._nome}")
        print(f"Login: {self._login}")
        print("Tipo de conta: Usuário comum ")

    
 