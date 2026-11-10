"""
Este código é a implementação da classe Usuario
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.usuario_cnt import Usuario_cnt
from src.models.BDManager_cnt import BDManager_cnt
from src.implement.livro_imp import Livro
 

class Usuario(Usuario_cnt):
#metodos comuns

    def __init__(self, nome, login, senha)->None:

        #verificação dos dados para login
        if not isinstance(nome, str):
            raise TypeError("O nome deve ser uma string")
        #if not nome.strip():
         #   raise ValueError("O nome não pode ser vazio")

        if not isinstance(login, str):
            raise TypeError("O login deve ser uma string")
        if not login.strip():
            raise ValueError("O login não pdoe ser vazio")

        if not isinstance(senha, str):
            raise TypeError("A senha deve ser uma string")
        if not senha.strip():
            raise ValueError("A senha não pdoe ser vazio")

        self._nome = nome
        self._login = login
        self.__senha = senha

        #dados relacionados a leitura
        self.__biblioteca_pessoal = []
        self.__biblioteca_desejo = []
        self.__livro_atual = None
        self.__livros_lidos = []
        self.__paginometro = {}
        self.__paginas_lidas_totais = 0
        self.__tempo_leitura_dia = {}
        self.__tempo_de_leitura_total = 0.0
        self.__preferencias_genero = []
        self.__livros_abandonados = []
        self.__amigos = []
        self.__trechos_pref = []
        self.__metas_leitura = []

    def construtor_bd(self, solicitante, dados: dict): 
    
        from src.implement.BDManager_imp import BDmanager
        if not isinstance(solicitante, BDmanager):
            raise TypeError("Solicitante sem autorização")

        # 1. Chamamos o __init__ para garantir que as validações base ocorram
        # e para criar os atributos que não vêm do banco (como paginas_lidas_totais)
        nome_bd = dados.get("nome", "")
        login_bd = dados.get("login", "")
        senha_bd = dados.get("_senha", "")
        self.__init__(nome_bd, login_bd, senha_bd)

        # 2. Mapeamento explícito de cada chave do BD para o atributo da classe
        self.__biblioteca_pessoal  = dados.get("_biblioteca_pessoal", [])
        self.__biblioteca_desejo   = dados.get("_biblioteca_desejo", [])
        self.__livro_atual = dados.get("_livro_atual") or None
        self.__livros_lidos        = dados.get("_livros_lidos", [])
        self.__paginometro         = dados.get("_paginometro", {})
        self.__preferencias_genero = dados.get("_preferencias_genero", [])
        self.__livros_abandonados  = dados.get("_livros_abandonados", [])
        self.__amigos              = dados.get("_amigos", [])
        self.__trechos_pref        = dados.get("_trechos_pref", [])
        self.__metas_leitura       = dados.get("_metas_leitura", [])
        
    def resumo_desempenho(self)->None:
        qntd_livro = len(self.__livros_lidos)
        print(f"Quantidade de livros lidos: {qntd_livro}")
        print(f"Tempo total de leitura: {self.__tempo_de_leitura_total} h")

    def ver_amigos(self)->list:
        return self.__amigos

    def definir_meta(self)->None:
        meta = input("Prefere definir uma meta de páginas ou livros?")
        #normalização de entradas
         #converte para letras minúsculas e retira espaço dos extremos
        meta = meta.strip().lower()

        if meta in ("paginas", "páginas"):
            alvo = int(input("Quantas paginas por mês?"))
            nova_meta = {"tipo": "paginas_por_mes", "alvo": alvo, "progresso": 0}
            self.__metas_leitura.append(nova_meta)

        elif meta == "livros":
            alvo = int(input("Quantos livros por ano?"))
            nova_meta = {"tipo": "livros_por_ano", "alvo": alvo, "progresso": 0}
            self.__metas_leitura.append(nova_meta)

        else:
            raise ValueError("Meta inválida")

    def consultar_metas_progresso(self)->None:
        if not self.__metas_leitura:
            print("Você não possui metas cadastradas")
            return 
        #percorre uma lista e em cada posição printa o dict
        for meta in self.__metas_leitura:
            if meta["tipo"] == "paginas_por_mes":
                print(f"Meta mensal de páginas: {meta['alvo']}")
                print(f"Progresso: {meta['progresso']} de {meta['alvo']} páginas")

            elif meta["tipo"] == "livros_por_ano":
                print(f"Meta anual de livros: {meta['alvo']}")
                print(f"Progresso: {meta['progresso']} de {meta['alvo']} livros")
    
    def registrar_tempo_leitura(self, tempo: float, data: str)->None:
        if not isinstance(tempo, (float,int)):
            raise TypeError("O tempo deve ser escrito numericamente") 
               
        if tempo < 0:
            raise ValueError("Tempo deve ser positivo")

        if not isinstance(data, str):
            raise TypeError('A data deve ser escrita no formato "dd/mm" ')
        
        #acumulando o tempo desde o inicio de uso
        self.__tempo_de_leitura_total += tempo
        #relaciona tempo gasto de leitura em cada dia
        self.__tempo_leitura_dia[data] = (self.__tempo_leitura_dia.get(data, 0) + tempo)

    def registrar_paginas_lidas(self, valor: int)->None:
        if not isinstance(valor,int):
            raise TypeError("A quantidade de páginas lidas deve ser um número inteiro")        
        
        if valor < 0:
            raise ValueError("Números de páginas deve ser positivo")

        self.__paginas_lidas_totais += valor

    def registrar_paginas_por_mes(self, mes: str, paginaslidas: int)->None:
        if not isinstance(mes, str):
            raise TypeError("O mês deve ser escrito por extenso")
        meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
                 "agosto", "setembro", "outubro", "novembro", "dezembro"]
        mes = mes.strip().lower()

        if mes not in meses:
            raise ValueError("Mês inválido")

        if not isinstance(paginaslidas, int):
            raise TypeError("A quantidade d epáginas lidas deve ser um número inteiro")
        
        if paginaslidas < 0:
            raise ValueError("O número de páginas lidas deve ser positivo")
        
        self.__paginometro[mes] = self.__paginometro.get(mes, 0) + paginaslidas 

        #atualizando o progresso da meta
        for meta in self.__metas_leitura:
            if meta["tipo"] == "paginas_por_mes":
                meta["progresso"] = self.__paginometro[mes]

    def seguir_pessoa(self, user:Usuario)->None:
        if not isinstance(user, Usuario):
            raise TypeError("O objeto deve ser uma instância de Usuario")
        if user.login == self.login:
            raise ValueError("Um usuário não pode seguir a si mesmo")

        if user.login in self.__amigos:
            raise ValueError("Você já segue esse usuário")

        self.__amigos.append(user.login)

    def cadastrar_livro_bp(self, livro:Livro, bd:BDManager_cnt)->None:
        if not isinstance(livro, Livro):
            raise TypeError("O livro indicado não é uma instância de Livro")

        if not isinstance(bd, BDManager_cnt):
            raise TypeError("O banco informado não é uma instância de BDmanager")
        
        if bd.validar_objeto(livro) == False:
            raise ValueError("Este livro não existe no banco de dados")
        
        if livro in self.__biblioteca_pessoal:
            raise ValueError("Esse livro já está cadastrado na sua biblioteca pessoal")
        
        self.__biblioteca_pessoal.append(livro)

    def adicionar_lista_desejo(self, livro: Livro, bd: BDManager_cnt)->None:
        if not isinstance(livro, Livro):
            raise TypeError("O livro indicado não é uma instância de Livro")

        if not isinstance(bd, BDManager_cnt):
            raise TypeError("O banco informado não é uma instância de BDmanager")
    
        if bd.validar_objeto(livro) == False:
            raise ValueError("Livro não consta no banco de dados")
        
        if livro in self.__biblioteca_desejo:
            raise ValueError("Esse livro já está cadastrado na sua lista de desejos")
        
        self.__biblioteca_desejo.append(livro)

    def remover_lista_desejo(self, livro: Livro, bd: BDManager_cnt)->None:
        if not isinstance(livro, Livro):
            raise TypeError("O livro indicado não é uma instância de Livro")

        if not isinstance(bd, BDManager_cnt):
            raise TypeError("O banco fornecido não é uma instância de BDmanager")

        if bd.validar_objeto(livro) == False:
            raise ValueError("Livro não exist eno banco de dados")

        if livro not in self.__biblioteca_desejo:
            raise ValueError("Esse livro não está cadastrado na sua lista de desejos")

        self.__biblioteca_desejo.remove(livro)


    def avaliar_livro(self, livro: Livro, nota: float, resenha: str)->None:
        if not isinstance(livro, Livro):
            raise TypeError("O livro não é uma instancia de Livro")

        if livro not in self.__livros_lidos:
            raise ValueError("Não é possível avaliar um livro que não foi lido")
        
        livro.avaliar(nota, resenha)

    def registrar_trecho(self, livro: Livro, trecho: str) -> None:
        if not isinstance(livro, Livro):
            raise TypeError("O objeto deve ser uma instância de Livro")

        if not isinstance(trecho, str):
            raise TypeError("O trecho deve ser uma string")

        if not trecho.strip():
            raise ValueError("O trecho não pode ser vazio")

        if livro not in self.__livros_lidos and livro != self.__livro_atual: # só entra no bloco se as duas condições forem true
            raise ValueError("Só é possivel registrar trechos de livros lidos ou em leitura")

        #os trechos pref são informações dadas pelo usuário e cada resgistro liga o trecho a um livro referente
        registro = {"livro": livro, "texto": trecho.strip()}
        self.__trechos_pref.append(registro) 

    def iniciar_leitura(self, livro: Livro, bd:BDManager_cnt)->None:
        if not  isinstance(livro, Livro):
            raise TypeError("O objeto informado não um Livro")

        if not isinstance(bd, BDManager_cnt):
            raise TypeError("O banco indicado deve ser uma instância de BDmanager")

        if self.__livro_atual is not None:
            raise ValueError("Já tem uma leitura em andamento")
        

        if not bd.validar_objeto(livro):
            raise ValueError("O livro não existe no banco de dados")

        self.__livro_atual = livro

    def concluir_leitura(self)->None:
        if self.__livro_atual is None:
            raise ValueError("Não há leitura em andamento para concluir")
        
        livroconcluido = self.__livro_atual
        self.__livros_lidos.append(livroconcluido)
        self.__livro_atual = None

        #atualizando progresso de meta livros por ano
        for meta in self.__metas_leitura:
            if meta["tipo"] == "livros_por_ano":
                meta["progresso"] += 1

    def abandonar_leitura(self)->None:
        if self.__livro_atual is None:
            raise ValueError("Não há leitura em andamento para abandonar")
        
        livroabandonado = self.__livro_atual
        self.__livros_abandonados.append(livroabandonado)
        self.__livro_atual = None

    def adicionar_preferencia(self, genero:str)->None:
        if not isinstance(genero, str):
            raise TypeError("O gênero deve ser escrito")
        
        genero_format = genero.strip()

        if not genero_format:
            raise ValueError("Gênero não pode ser vazio")

        if genero_format.lower() in [g.lower() for g in self.__preferencias_genero]:
            raise ValueError("Esse gênero já está nas preferências")
        
        self.__preferencias_genero.append(genero_format)
      
    def remover_preferencia(self, genero:str)->None:#list comprehension: evita bugs e é mais rápida que o for tradicional
        if not isinstance(genero, str):
            raise TypeError("O genero deve ser uma string")

        genero = genero.strip()

        if not genero:
            raise ValueError("O gênero não pode estar vazio")

        if genero.lower() not in [gen.lower() for gen in self.__preferencias_genero]:
            raise ValueError("O gênero informado não está nas preferências")
        
        self.__preferencias_genero =[gen for gen in self.__preferencias_genero if gen != genero]

    def consultar_preferencia(self)->list:
        return self.__preferencias_genero

#getters
    @property
    def nome(self):
        return self._nome

    @property
    def login(self):
        return self._login

    @property
    def biblioteca_pessoal(self):
        return self.__biblioteca_pessoal

    @property
    def biblioteca_desejo(self):
        return self.__biblioteca_desejo

    @property
    def livro_atual(self):
        return self.__livro_atual

    @property
    def livros_lidos(self):
        return self.__livros_lidos

    @property
    def paginometro(self):
        return self.__paginometro

    @property
    def paginas_lidas_totais(self):
        return self.__paginas_lidas_totais

    @property
    def tempo_leitura_dia(self):
        return self.__tempo_leitura_dia

    @property
    def tempo_de_leitura_total(self):
        return self.__tempo_de_leitura_total

    @property
    def livros_abandonados(self):
        return self.__livros_abandonados
    









