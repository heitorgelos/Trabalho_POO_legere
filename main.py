"""
Arquivo main, usa dos recursos nas pastas de modelo (contrato) e implementação
"""
from src.implement.BDManager_imp import BDmanager
from src.implement.usuario_gerente_imp import UsuarioGerente
from src.interface import tela_inicial, menu_comum, menu_gerente


def main():
    banco = BDmanager()

    try:
        banco.carregar_database()
    except Exception as erro:
        print(f"Não foi possível carregar o banco de dados: {erro}")
        return

    while True:
        usuario = tela_inicial(banco)

        if usuario is None:
            print("\nAté mais!")
            break

        if isinstance(usuario, UsuarioGerente):
            menu_gerente(usuario, banco)
        else:
            menu_comum(usuario, banco)


if __name__ == "__main__":
    main()