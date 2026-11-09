"""
Arquivo principal, usa dos recursos nas pastas de modelo (contrato) e implementação.
"""

from src.implement.BDManager_imp import BDmanager
from src.implement.usuario_comum_imp import UsuarioComum
from src.implement.usuario_gerente_imp import UsuarioGerente
import src.interface as Interface

def main():

    bd = BDmanager()
    bd.carregar_database()

    sistema_rodando = True

    while(sistema_rodando):

        user = Interface.tela_inicial(bd)
        if user is None:
            if Interface.continuar_ou_sair() == False: 
                sistema_rodando = False
                continue

        if isinstance(user, UsuarioComum):
            print("debug: entrando menu comum")
            Interface.menu_gerente(user, bd)

        elif isinstance(user, UsuarioGerente):
            print("debug: entrando menu gerente")
            Interface.menu_comum(user, bd)

        else:
            print("ERRO: Nenhum menu definido")

if __name__ == "__main__":
    main()