"""
Este código é a implementação da classe BDmanager.
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.BDManager_cnt import BDManager_cnt
from src.implement.usuario_comum_imp import UsuarioComum
from src.implement.usuario_gerente_imp import UsuarioGerente
from src.implement.livro_imp import Livro
from pathlib import Path
import pandas as pd, json

class BDmanager(BDManager_cnt):
    def __init__(self):
        self._df_livros = pd.DataFrame()
        self._df_pessoas = pd.DataFrame()

    def carregar_database(self) -> bool:
        diretorio_atual = Path(__file__).resolve().parent.parent #Pegando o diretorio dos dados

        #Obtendo os livros
        caminho_csv = diretorio_atual / "database" /"livros_ficticios.csv"

        df_livros = pd.read_csv(caminho_csv)
        df_livros["_resenhas"] = df_livros["_resenhas"].apply(json.loads) #Aqui se pega a coluna de resenhas e se quebra em uma lista

        #Obtendo as pessoas
        caminho_csv = diretorio_atual / "database" /"usuarios_comuns_ficticios.csv"

        df_pessoas = pd.read_csv(caminho_csv)
    
        def _parse_json(x, padrao):
            if isinstance(x, str) and x.strip():
                return json.loads(x)
            return padrao  # vazio/NaN vira o padrão

        #Colunas que empacotam dados
        COLUNAS_JSON = {
            "_biblioteca_pessoal": list,
            "_biblioteca_desejo": list,
            "_livros_lidos": list,
            "_paginometro": dict,
            "_tempo_leitura_dia": dict,
            "_preferencias_genero": list,
            "_livros_abandonados": list,
            "_amigos": list,
            "_trechos_pref": list,
            "_metas_leitura": list,
        }

        #Aplicando o desempacotamento json
        for col, tipo in COLUNAS_JSON.items():
            df_pessoas[col] = df_pessoas[col].apply(lambda x, t=tipo: _parse_json(x, t()))

        df_pessoas["_livro_atual"] = df_pessoas["_livro_atual"].fillna("")
        #df_pessoas["_tempo_medio_leitura_min_dia"] = df_pessoas["_tempo_medio_leitura_min_dia"].fillna(0)
        df_pessoas["nome"] = df_pessoas["nome"].fillna("")

        self._df_livros = df_livros
        self._df_pessoas = df_pessoas
        return True
    
    def validar_objeto(self, obj) -> tuple[bool, any]:

        if isinstance(obj, (UsuarioComum, UsuarioGerente)): 

            #Aqui eu vou checar se o nome do usuário existe no df
            linha_alvo = self._df_pessoas[self._df_pessoas["login"] == obj.login]
            if len(linha_alvo)==0:
                return False, None 

            #Pegando o índice da linha
            linha_idx = linha_alvo.index[0]

            #Pegando os dicionarios e comparando
            linha_dict = self._df_pessoas.iloc[linha_idx].to_dict()
            if isinstance(obj, UsuarioComum):
                obj_cmp = UsuarioComum.__new__(UsuarioComum)
            else: 
                obj_cmp = UsuarioGerente.__new__(UsuarioGerente)
            obj_cmp.__dict__ = linha_dict
            cmp = (
                obj_cmp.__dict__["login"] == obj.__dict__["_login"]
                and obj_cmp.__dict__["_senha"] == obj.__dict__["_Usuario__senha"]
            )
            
            obj_cmp.construtor_bd(self, linha_dict)
            
            #print("Pessoa encontrada")
            #print(obj_cmp.__dict__)
            
            return cmp, obj_cmp

        elif isinstance(obj, Livro): #Mesma lógica
            linha_alvo = self._df_livros[self._df_livros["titulo"]==obj.titulo]
            if len(linha_alvo)==0:
                print("Livro não existe")
                return False, None
            linha_idx = linha_alvo.index[0]
            linha_dict = self._df_livros.iloc[linha_idx].to_dict()
            obj_cmp = Livro.__new__(Livro)
            obj_cmp.__dict__ = linha_dict
            cmp = (obj_cmp.__dict__["titulo"] == obj.__dict__["_titulo"] and obj_cmp.__dict__["autor"] == obj.__dict__["_autor"])
            print("Dicionario recebido do dataframe: ",linha_dict)
            return cmp, obj

        else: 
            raise TypeError("Objeto inserido não é de um dos tipos reconhecidos pelo sistema")
        
    def salvar_database(self, caminho:str, COLUNAS_JSON:list, df_rec:pd.DataFrame) -> bool:
        df = df_rec.copy()  # copia pra não destruir as listas em memória

        for col in COLUNAS_JSON:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False))

        df.to_csv(caminho, index=False, encoding="utf-8-sig")

        return True

    def atualizar_objeto(self, obj_original) -> bool: 
        #Caminho de salvamento
        RAIZ = Path(__file__).resolve().parents[2]
        PASTA_DB = RAIZ / "src" / "database"

        caminho_pessoas = PASTA_DB /"usuarios_comuns_ficticios_2.csv"
        caminho_livros  = PASTA_DB / "livros_ficticios_2.csv"

        if isinstance(obj_original, (UsuarioComum, UsuarioGerente)):
            is_user_true, obj_cmp = self.validar_objeto(obj_original)

            if is_user_true:
                print("Existência de usuário verificada")
                mask = self._df_pessoas["login"] == obj_original.login   # login em vez de nome (nome pode ser vazio)
                idx = self._df_pessoas.index[mask][0] #Pego o índice da minha linha que possui os dados do objeto

                for coluna in self._df_pessoas.columns:
                    if coluna in ("nome", "login"):
                        valor = getattr(obj_original, coluna)  #Pega os atributos simples          
                    else:
                        valor = getattr(obj_original, f"_Usuario_{coluna}", None) #Pega os atributos das colunas protegidas (python faz o name mangling colonado antes o nome da classe)
                        print(valor)
                    self._df_pessoas.at[idx, coluna] = valor              

            #Aqui se filtra as colunas que não possuem listas pra poder empacotar tudo usando json
            colunas_json = [c for c in self._df_pessoas.columns if c not in ("nome", "login", "_senha", "_livro_atual")]
            self.salvar_database(caminho_pessoas, colunas_json, self._df_pessoas)

        elif isinstance(obj_original, Livro):
            is_user_true, obj_cmp = self.validar_objeto(obj_original)

            if is_user_true:
                print("Existência de livro verificada")
                mask = self._df_livros["titulo"] == obj_original.titulo   # nome é único para todos
                idx = self._df_livros.index[mask][0] #Pego o índice da minha linha que possui os dados do objeto

                for coluna in self._df_livros.columns:
                    valor = getattr(obj_original, coluna)  #Pega os atributos simples          
                    self._df_livros.at[idx, coluna] = valor  
                    print("Valor inserido: ", valor)                 

            #Aqui se filtra as colunas que não possuem listas pra poder empacotar tudo usando json
            colunas_json = ["resenhas"]
            self.salvar_database(caminho_livros, colunas_json, self._df_livros)

        else: 
            raise ValueError("Objeto inserido desconhecido")

        return True

    def cadastrar_objeto(self, obj) -> bool:
        RAIZ = Path(__file__).resolve().parents[2]
        caminho_pessoas = RAIZ / "src" / "database" / "usuarios_comuns_ficticios_2.csv"

        if isinstance(obj, (UsuarioComum, UsuarioGerente)):
            if (self._df_pessoas["login"] == obj.login).any():
                raise ValueError("Já existe um usuário com esse login")

            linha = []
            for coluna in self._df_pessoas.columns:
                if coluna in ("nome", "login"):
                    linha.append(getattr(obj, coluna))
                else:
                    linha.append(getattr(obj, f"_Usuario_{coluna}"))  # fazendo o name mangling

            self._df_pessoas.loc[len(self._df_pessoas)] = linha

            colunas_json = [c for c in self._df_pessoas.columns
                            if c not in ("nome", "login", "_senha", "_livro_atual")] #Separando as colunas que nao sao compactadas em JSON
            self.salvar_database(caminho_pessoas, colunas_json, self._df_pessoas)
        return True

"""
def test(): 
    bd1 = BDmanager()
    bd1.carregar_database()
    l1 = Livro("A Sombra no Porão","Marcos Valadares", 2018,312,"terror","Editora Noite Alta","Uma família descobre que o porão da casa nova guarda algo que se alimenta do medo.","67+")
    print(bd1.validar_objeto(l1))
    print("ATRIBUTOS: ",l1.autor, l1.categoria, l1.descricao)
    print(bd1.atualizar_objeto(l1))

test()

def test(): 
    bd1 = BDmanager()
    bd1.carregar_database()
    p1 = UsuarioComum('', 'teste','1234')
    l1 = Livro("A Sombra no Porão","Marcos Valadares", 2018,312,"terror","Editora Noite Alta","Uma família descobre que o porão da casa nova guarda algo que se alimenta do medo.","16+")
    
    
    TESTE FUNCIONOU!
    ret = bd1.validar_objeto(p1)
    print("Validação da pessoa: ",ret)
    ret = bd1.validar_objeto(l1)
    print("Validação do livro: ",ret)

    Atributos privados prejudicam bastante mas está funcionando
    
    p1.nome = "6767"
    bd1.atualizar_objeto(p1)
    l1.descricao = "76"
    bd1.atualizar_objeto(l1)
    
    
    

test()
"""