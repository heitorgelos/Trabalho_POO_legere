"""Interface do sistema Legere"""

import os
import io
from contextlib import redirect_stdout

from src.implement.usuario_comum_imp import UsuarioComum
from src.implement.usuario_gerente_imp import UsuarioGerente
from src.implement.livro_imp import Livro
from src.implement.clube_livro_imp import ClubeLivro


def limpar_tela():
    """Limpa o terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def titulo(texto):
    limpar_tela()
    print("=" * 52)
    print(f" {texto}")
    print("=" * 52)


def ler_opcao(mensagem, opcoes):
    """Lê uma opção e repete até receber uma escolha válida."""
    while True:
        opcao = input(mensagem).strip()
        if opcao in opcoes:
            return opcao
        print("Opção inválida. Tente novamente.")


def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("Digite um número válido.")


def executar(acao):
    """Executa uma operação sem deixar erros de entrada derrubarem o programa."""
    try:
        resultado = acao()
        if resultado is not False:
            print("\nOperação realizada.")
        return resultado
    except (ValueError, TypeError, KeyError, IndexError) as erro:
        print(f"\nNão foi possível realizar a operação: {erro}")
    except Exception as erro:
        print(f"\nOcorreu um erro inesperado: {erro}")
    return None


def salvar_usuario(usuario, bd):
    """Pede ao banco que atualize o usuário."""
    try:
        with redirect_stdout(io.StringIO()):
            bd.atualizar_objeto(usuario)
        print("\nAtualização enviada ao banco de dados.")
    except Exception as erro:
        print(f"\nAs alterações continuam na sessão, mas não foram salvas: {erro}")


def listar_livros(bd):
    """Mostra o catálogo disponível."""
    if bd._df_livros.empty:
        print("Nenhum livro foi encontrado.")
        return

    for indice, linha in bd._df_livros.iterrows():
        print(f"{indice + 1}. {linha['titulo']} — {linha['autor']}")


def buscar_livro(bd):
    """Localiza um livro pelo título e devolve um objeto Livro."""
    titulo_livro = input("Digite o título (ou parte dele): ").strip().lower()
    if not titulo_livro:
        print("Digite um título.")
        return None

    encontrados = bd._df_livros[
        bd._df_livros["titulo"].astype(str).str.lower().str.contains(
            titulo_livro, na=False
        )
    ]

    if encontrados.empty:
        print("Nenhum livro encontrado.")
        return None

    print("\nLivros encontrados:")
    linhas = list(encontrados.iterrows())
    for posicao, (_, linha) in enumerate(linhas, start=1):
        print(f"{posicao}. {linha['titulo']} — {linha['autor']}")

    escolha = ler_opcao(
        "\nEscolha o livro (0 para cancelar): ",
        [str(i) for i in range(len(linhas) + 1)]
    )
    if escolha == "0":
        return None

    linha = linhas[int(escolha) - 1][1]
    livro = Livro(
        str(linha["titulo"]),
        str(linha["autor"]),
        int(linha["ano"]),
        int(linha["num_paginas"]),
        str(linha["categoria"]),
        str(linha["editora"]),
        str(linha["descricao"]),
        str(linha["faixa_etaria"])
    )
    livro._estrelas = float(linha.get("_estrelas", 0) or 0)
    resenhas = linha.get("_resenhas", [])
    livro._resenhas = resenhas if isinstance(resenhas, list) else []
    return livro


def mostrar_livros_usuario(titulo_lista, livros):
    print(f"\n{titulo_lista}:")
    if not livros:
        print("  Nenhum livro cadastrado.")
        return
    for numero, livro in enumerate(livros, start=1):
        nome = livro.titulo if isinstance(livro, Livro) else str(livro)
        print(f"  {numero}. {nome}")


def localizar_usuario(login, bd):
    """Busca um usuário cadastrado sem precisar conhecer sua senha."""
    linhas = bd._df_pessoas[bd._df_pessoas["login"] == login]
    if linhas.empty:
        return None

    dados = linhas.iloc[0].to_dict()
    usuario = UsuarioComum.__new__(UsuarioComum)
    usuario.construtor_bd(bd, dados)
    return usuario


def get_clube_moderador():
    cl1 = ClubeLivro(None)
    
    if cl1.carregar_dados():
        print("Moderador recuperado!")
        return cl1.moderador
    else: 
        
        return None
    
def tela_inicial(bd):
    while True:
        titulo("LEGERE — CONTROLE DE LEITURA")
        print("1. Entrar")
        print("2. Criar conta")
        print("0. Sair")

        opcao = ler_opcao("\nEscolha: ", ["0", "1", "2"])

        if opcao == "0":
            return None

        if opcao == "2":
            titulo("CRIAR CONTA")
            nome = input("Nome: ").strip()
            login = input("Login: ").strip()
            senha = input("Senha: ").strip()
            print("\nTipo de conta:")
            print("1. Leitor")
            print("2. Gerente")
            tipo = ler_opcao("Escolha: ", ["1", "2"])

            try:
                if tipo == "1":
                    novo_usuario = UsuarioComum(nome, login, senha)
                else:
                    novo_usuario = UsuarioGerente(nome, login, senha)

                bd.cadastrar_objeto(novo_usuario)
                if tipo == "2":
                    if not hasattr(bd, "_gerentes_interface"):
                        bd._gerentes_interface = set()
                    bd._gerentes_interface.add(login)

                print("\nConta criada com sucesso!")
                pausar()
                return novo_usuario
            except Exception as erro:
                print(f"\nNão foi possível criar a conta: {erro}")
                pausar()
                continue

        titulo("LOGIN")
        login = input("Login: ").strip()
        senha = input("Senha: ").strip()

        try:
            
            gerente = get_clube_moderador()
            if None!= gerente and login == gerente[0]:
                
                busca = UsuarioGerente("", login, senha)
                valido, usuario = bd.validar_objeto(busca)
            else:
                
                busca = UsuarioComum("", login, senha)
                valido, usuario = bd.validar_objeto(busca)

            if valido:
                print(f"\nBem-vindo(a), {usuario.nome}!")
                pausar()
                return usuario

            print("\nLogin ou senha incorretos.")
        except Exception as erro:
            print(f"\nNão foi possível entrar: {erro}")
        pausar()


def menu_perfil(usuario, bd):
    while True:
        titulo("MEU PERFIL E PREFERÊNCIAS")
        usuario.consultar_perfil()
        print(f"Preferências: {', '.join(usuario.consultar_preferencia()) or 'Nenhuma'}")
        print("\n1. Adicionar preferência")
        print("2. Remover preferência")
        print("3. Ver pessoas que sigo")
        print("4. Seguir uma pessoa")
        print("0. Voltar")

        opcao = ler_opcao("\nEscolha: ", ["0", "1", "2", "3", "4"])
        if opcao == "0":
            return
        elif opcao == "1":
            genero = input("Gênero literário: ").strip()
            executar(lambda: usuario.adicionar_preferencia(genero))
            salvar_usuario(usuario, bd)
        elif opcao == "2":
            genero = input("Gênero a remover: ").strip()
            executar(lambda: usuario.remover_preferencia(genero))
            print("Observação: há um erro no método de remoção da implementação atual.")
            salvar_usuario(usuario, bd)
        elif opcao == "3":
            amigos = usuario.ver_amigos()
            print("\nPessoas que você segue:")
            print("\n".join(amigos) if amigos else "Você ainda não segue ninguém.")
            pausar()
        else:
            login = input("Login da pessoa: ").strip()
            pessoa = localizar_usuario(login, bd)
            if pessoa is None:
                print("Usuário não encontrado.")
            else:
                executar(lambda: usuario.seguir_pessoa(pessoa))
                salvar_usuario(usuario, bd)
            pausar()


def menu_biblioteca(usuario, bd):
    while True:
        titulo("BIBLIOTECA E LIVROS")
        print("1. Consultar catálogo")
        print("2. Ver minha biblioteca")
        print("3. Ver lista de desejos")
        print("4. Adicionar livro à biblioteca")
        print("5. Adicionar livro à lista de desejos")
        print("6. Remover livro da lista de desejos")
        print("7. Iniciar leitura")
        print("8. Concluir leitura atual")
        print("9. Abandonar leitura atual")
        print("10. Avaliar livro lido")
        print("11. Registrar trecho favorito")
        print("12. Ver trechos preferidos")
        print("0. Voltar")

        opcao = ler_opcao("\nEscolha: ", [str(i) for i in range(12)])

        if opcao == "0":
            return
        elif opcao == "1":
            titulo("CATÁLOGO DE LIVROS")
            listar_livros(bd)
            pausar()
        elif opcao == "2":
            titulo("MINHA BIBLIOTECA")
            mostrar_livros_usuario("Livros lidos", usuario.livros_lidos)
            mostrar_livros_usuario("Biblioteca pessoal", usuario.biblioteca_pessoal)
            mostrar_livros_usuario("Livros abandonados", usuario.livros_abandonados)
            pausar()
        elif opcao == "3":
            titulo("LISTA DE DESEJOS")
            mostrar_livros_usuario("Livros desejados", usuario.biblioteca_desejo)
            pausar()
        elif opcao in ("4", "5", "6", "7", "10", "11"):
            livro = buscar_livro(bd)
            if livro is None:
                pausar()
                continue

            if opcao == "4":
                executar(lambda: usuario.cadastrar_livro_bp(livro, bd))
            elif opcao == "5":
                executar(lambda: usuario.adicionar_lista_desejo(livro, bd))
            elif opcao == "6":
                # A lista pode conter títulos em texto ou objetos Livro.
                existente = next(
                    (item for item in usuario.biblioteca_desejo
                     if (item.titulo if isinstance(item, Livro) else str(item)).lower()
                     == livro.titulo.lower()),
                    None
                )
                if existente is None:
                    print("Esse livro não está na sua lista de desejos.")
                else:
                    executar(lambda: usuario.remover_lista_desejo(existente, bd))
            elif opcao == "7":
                executar(lambda: usuario.iniciar_leitura(livro, bd))
            elif opcao == "10":
                nota = ler_float("Nota (0 a 5): ")
                resenha = input("Escreva sua resenha: ").strip()
                executar(lambda: usuario.avaliar_livro(livro, nota, resenha))
            else:
                trecho = input("Trecho favorito: ").strip()
                executar(lambda: usuario.registrar_trecho(livro, trecho))
            salvar_usuario(usuario, bd)
            pausar()
        elif opcao == "8":
            executar(usuario.concluir_leitura)
            salvar_usuario(usuario, bd)
            pausar()
        elif opcao == "9":
            executar(usuario.abandonar_leitura)
            salvar_usuario(usuario, bd)
            pausar()



def menu_desempenho(usuario, bd):
    while True:
        titulo("DESEMPENHO E METAS")
        usuario.resumo_desempenho()
        print(f"Páginas lidas no total: {usuario.paginas_lidas_totais}")
        print(f"Tempo total: {usuario.tempo_de_leitura_total} hora(s)")
        print("\n1. Consultar metas")
        print("2. Criar meta")
        print("3. Registrar páginas de um mês")
        print("4. Registrar tempo de leitura")
        print("5. Registrar páginas lidas")
        print("0. Voltar")

        opcao = ler_opcao("\nEscolha: ", ["0", "1", "2", "3", "4", "5"])
        if opcao == "0":
            return
        elif opcao == "1":
            usuario.consultar_metas_progresso()
        elif opcao == "2":
            executar(usuario.definir_meta)
        elif opcao == "3":
            mes = input("Mês por extenso: ").strip()
            paginas = ler_int("Quantidade de páginas: ")
            executar(lambda: usuario.registrar_paginas_por_mes(mes, paginas))
        elif opcao == "4":
            tempo = ler_float("Tempo em horas: ")
            data = input("Data (dd/mm): ").strip()
            executar(lambda: usuario.registrar_tempo_leitura(tempo, data))
        else:
            paginas = ler_int("Quantidade de páginas lidas: ")
            executar(lambda: usuario.registrar_paginas_lidas(paginas))

        salvar_usuario(usuario, bd)
        pausar()


def menu_comum(usuario: UsuarioComum, bd):
    while True:
        titulo(f"PAINEL DO LEITOR — {usuario.nome}")
        print("1. Meu perfil e preferências")
        print("2. Minha biblioteca e livros")
        print("3. Desempenho e metas")
        print("4. Leitura atual")
        print("5. Salvar alterações")
        print("0. Fazer logout")

        opcao = ler_opcao("\nO que deseja fazer? ", ["0", "1", "2", "3", "4", "5"])
        if opcao == "0":
            salvar_usuario(usuario, bd)
            print("\nLogout realizado.")
            pausar()
            return
        elif opcao == "1":
            menu_perfil(usuario, bd)
        elif opcao == "2":
            menu_biblioteca(usuario, bd)
        elif opcao == "3":
            menu_desempenho(usuario, bd)
        elif opcao == "4":
            titulo("LEITURA ATUAL")
            atual = usuario.livro_atual
            if atual is None or atual == "":
                print("Você não tem uma leitura em andamento.")
            else:
                nome = atual.titulo if isinstance(atual, Livro) else str(atual)
                print(f"Livro atual: {nome}")
                print("\n1. Concluir leitura")
                print("2. Abandonar leitura")
                print("0. Voltar")
                acao = ler_opcao("Escolha: ", ["0", "1", "2"])
                if acao == "1":
                    executar(usuario.concluir_leitura)
                    salvar_usuario(usuario, bd)
                elif acao == "2":
                    executar(usuario.abandonar_leitura)
                    salvar_usuario(usuario, bd)
                pausar()
        else:
            salvar_usuario(usuario, bd)
            pausar()


def menu_clube(usuario: UsuarioGerente, bd):
    while True:
        titulo("CLUBE DO LIVRO")
        clube = usuario.clube
        if clube is None:
            print("Você ainda não criou um clube.")
            print("1. Criar clube")
            print("0. Voltar")
            opcao = ler_opcao("\nEscolha: ", ["0", "1"])
            if opcao == "0":
                return
            executar(usuario.criar_clube)
            clube = usuario.clube
            if clube is not None:
                if not clube.nome:
                    clube.nome.append("")
                nome = input("Nome do clube: ").strip()
                executar(lambda: usuario.nomear_clube(clube, nome))
            pausar()
            continue

        nome_clube = clube.nome[0] if clube.nome else "(sem nome)"
        print(f"Clube: {nome_clube}")
        print(f"Moderador: {', '.join(clube.moderador) or 'Nenhum'}")
        print(f"Membros: {', '.join(clube.membros) or 'Nenhum'}")
        print(f"Livros: {', '.join(clube.livros) or 'Nenhum'}")
        print("\n1. Adicionar participante")
        print("2. Remover participante")
        print("3. Adicionar livro")
        print("4. Ver pessoas expulsas")
        print("5. Alterar nome")
        print("6. Passar moderação")
        print("7. Excluir clube")
        print("8. Carregar dados do clube")
        print("9. Salvar dados do clube")
        print("0. Voltar")

        opcao = ler_opcao("\nEscolha: ", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        if opcao == "0":
            return
        elif opcao == "1":
            login = input("Login do participante: ").strip()
            pessoa = localizar_usuario(login, bd)
            if pessoa is None:
                print("Usuário não encontrado.")
            else:
                executar(lambda: usuario.adicionar_participante(clube, pessoa))
        elif opcao == "2":
            login = input("Login do participante: ").strip()
            pessoa = localizar_usuario(login, bd)
            if pessoa is None:
                print("Usuário não encontrado.")
            else:
                executar(lambda: usuario.remover_participante(clube, pessoa))
        elif opcao == "3":
            livro = buscar_livro(bd)
            if livro is not None:
                executar(lambda: usuario.adicionar_livro(clube, livro))
        elif opcao == "4":
            expulsos = executar(lambda: usuario.ver_expulsos(clube))
            print("\nPessoas expulsas:", ", ".join(expulsos or []) or "Nenhuma")
        elif opcao == "5":
            nome = input("Novo nome: ").strip()
            executar(lambda: usuario.nomear_clube(clube, nome))
        elif opcao == "6":
            login = input("Login do novo moderador: ").strip()
            novo = localizar_usuario(login, bd)
            if novo is None:
                print("Usuário não encontrado.")
            else:
                novo_gerente = UsuarioGerente(novo.nome, novo.login, "temporaria")
                executar(lambda: usuario.passar_moderacao(clube, novo_gerente))
                print("Atenção: a implementação não transfere o clube para o atributo do novo gerente.")
        elif opcao == "7":
            confirmar = input("Tem certeza que deseja excluir o clube? (s/n): ").strip().lower()
            if confirmar == "s":
                executar(lambda: usuario.deletar_clube(clube))
        elif opcao == "8":
            executar(clube.carregar_dados)
        elif opcao == "9":
            executar(clube.salvar_dados)
        pausar()


def menu_gerente(usuario: UsuarioGerente, bd):
    while True:
        titulo(f"PAINEL DO GERENTE — {usuario.nome}")
        print("1. Meu perfil e preferências")
        print("2. Minha biblioteca e livros")
        print("3. Desempenho e metas")
        print("4. Leitura atual")
        print("5. Administrar clube do livro")
        print("6. Salvar alterações")
        print("0. Fazer logout")

        opcao = ler_opcao("\nO que deseja fazer? ", ["0", "1", "2", "3", "4", "5", "6"])
        if opcao == "0":
            salvar_usuario(usuario, bd)
            print("\nLogout realizado.")
            pausar()
            return
        elif opcao == "1":
            menu_perfil(usuario, bd)
        elif opcao == "2":
            menu_biblioteca(usuario, bd)
        elif opcao == "3":
            menu_desempenho(usuario, bd)
        elif opcao == "4":
            titulo("LEITURA ATUAL")
            atual = usuario.livro_atual
            print(
                atual.titulo if isinstance(atual, Livro) else
                (atual or "Nenhuma leitura em andamento.")
            )
            pausar()
        elif opcao == "5":
            menu_clube(usuario, bd)
        else:
            salvar_usuario(usuario, bd)
            pausar()
