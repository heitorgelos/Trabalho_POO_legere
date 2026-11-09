import os
from src.implement.usuario_comum_imp import UsuarioComum
from src.implement.usuario_gerente_imp import UsuarioGerente
from src.implement.livro_imp import Livro

def limpar_tela():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def tela_inicial(bd):
    limpar_tela()

    # esse tipo de texto eu usei no trabalho de PDS 2 e tb eh o jeito
    # que IA costuma fazer, talvez podemos modificar
    print("========================================")
    print("  BEM VINDO AO SEU CONTROLE DE LEITURA  ")
    print("========================================")
    print("1. Fazer Login")
    print("0. Sair")
    print("========================================")

    opcao = input("Como deseja iniciar? ").strip()

    if opcao == "0":
        return None

    elif opcao == "1":
        limpar_tela()
        print("Digite seu Login:\n")
        login = input("Login: ").strip()
        senha = input("Senha: ").strip()

        try:
            # ve se eh usuario comum
            busca_comum = UsuarioComum("", login, senha)
            is_valid, user_real = bd.validar_objeto(busca_comum) # p seguir como está em BDManager

            if is_valid:
                # print e input para visualizar funcionamento
                print(f"Bem vindo(a) {user_real.nome}")
                input("aperte enter") # esses "aperte enter" eh so pra eu ver as coisas acontecendo, serao removidos
                return user_real
            
            # agr ve se eh usuario gerente
            busca_gerente = UsuarioGerente("", login, senha)
            is_valid, user_real = bd.validar_objeto(busca_gerente)

            if is_valid:
                # print e input para visualizar funcionamento
                print(f"Bem vindo(a) {user_real.nome}")
                input("aperte enter")
                return user_real

            print("Login inválido ou não encontrado.")
            input("login errado (aperte enter)") # para testar

        except Exception as e: # talvez trocar o exception depois
            print(f"Erro relacionado ao banco de dados: {e}")
            input("aperte enter")
            return None

    else:
        print("Opção Inválida: selecione 0, 1 ou 2.")
        input("aperte enter")

def continuar_ou_sair():
    limpar_tela()
    
    print("0. Sair")
    print("1. Tela inicial")
    
    opcao = input("Como deseja prosseguir?").strip()

    if opcao == "0":
        return False
    return True

def menu_comum(usuario: UsuarioComum, bd):
    while True:
        limpar_tela()
        print("========================================")
        print(f"      PAINEL DO LEITOR: {usuario.nome}  ")
        print("========================================")
        print("1. Meu Perfil e Preferências")
        print("2. Minha Biblioteca e Livros")
        print("3. Desempenho e Metas de Leitura")
        print("4. Leitura Atual")
        print("0. Fazer Logout")
        print("========================================")
        
        opcao = input("O que deseja fazer? ").strip()
        
        match opcao:
            case "0":
                print("\nSaindo da conta...")
                input("Aperte ENTER para voltar à tela inicial...")
                break
                
            case "1":
                limpar_tela()
                print("--- MEU PERFIL ---")
                usuario.consultar_perfil()
                print(f"Preferências de Gênero: {usuario.consultar_preferencia()}")
                input("\nAperte ENTER para voltar...")
                
            case "2":
                limpar_tela()
                print("--- MINHA BIBLIOTECA ---")
                print(f"Biblioteca Pessoal: {len(usuario.biblioteca_pessoal)} livros")
                print(f"Lista de Desejos: {len(usuario.biblioteca_desejo)} livros")
                print(f"Livros Lidos: {len(usuario.livros_lidos)} livros")
                input("\nAperte ENTER para voltar...")
                
            case "3":
                limpar_tela()
                print("--- DESEMPENHO E METAS ---")
                usuario.resumo_desempenho()
                print("\nMetas cadastradas:", usuario.consultar_metas())
                input("\nAperte ENTER para voltar...")
                
            case "4":
                limpar_tela()
                print("--- LEITURA ATUAL ---")
                print(f"Livro atual: {usuario.livro_atual if usuario.livro_atual else 'Nenhum no momento'}")
                input("\nAperte ENTER para voltar...")
                
            case _:
                print("\nOpção Inválida.")
                input("Aperte ENTER para tentar novamente.")
                       
def menu_gerente(usuario: UsuarioGerente, bd):
    pass