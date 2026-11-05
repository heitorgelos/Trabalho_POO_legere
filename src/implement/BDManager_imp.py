"""
Este código é a implementação da classe BDmanager.
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.BDManager_cnt import BDManager_cnt
from pathlib import Path
import pandas as pd, json

class UsuarioComum():
    def __init__(self):
        self.id = 0
        pass

class Livro():
    def __init__(self):
        self.nome = "Hello world"
        pass

class BDmanager(BDManager_cnt):
    def __init__(self):
        self._df_livros = pd.DataFrame()
        self._df_pessoas = pd.DataFrame()

    def carregar_database(self):
        diretorio_atual = Path(__file__).resolve().parent.parent #Pegando o diretorio dos dados

        caminho_csv = diretorio_atual / "database" /"livros_ficticios.csv"

        df_livros = pd.read_csv(caminho_csv)
        df_livros["resenhas"] = df_livros["resenhas"].apply(json.loads) #Aqui se pega a coluna de resenhas e se quebra em uma lista
        #print(df_livros.head(n=1))
        #print(df_livros.info())

        caminho_csv = diretorio_atual / "database" /"usuarios_comuns_ficticios.csv"
        
        df_pessoas = pd.read_csv(caminho_csv)
        df_pessoas["biblioteca_pessoal"] = df_pessoas["biblioteca_pessoal"].apply(json.loads) 
        df_pessoas["biblioteca_desejo"] = df_pessoas["biblioteca_desejo"].apply(json.loads)
        df_pessoas["livros_lidos"] = df_pessoas["livros_lidos"].apply(json.loads) 
        df_pessoas["preferencias_genero"] = df_pessoas["preferencias_genero"].apply(json.loads) 
        df_pessoas["livros_abandonados"] = df_pessoas["livros_abandonados"].apply(json.loads) 
        df_pessoas["amigos"] = df_pessoas["amigos"].apply(json.loads)
        df_pessoas["trechos_pref"] = df_pessoas["trechos_pref"].apply(json.loads) 
        df_pessoas["metas_leitura"] = df_pessoas["metas_leitura"].apply(json.loads) 

        
        print(df_pessoas.biblioteca_pessoal)

        self._df_livros = df_livros
        self.df_livros = df_pessoas
        return True
    
    def validar_objeto(self, obj):
        if isinstance(obj, UsuarioComum): 
            #Aqui eu vou checar se o id do usuário existe no df
            linha_alvo = self._df_pessoas[self._df_pessoas["login"] == obj.login]
            if len(linha_alvo)==0:
                return False
            #obj_cmp = UsuarioComum() aqui eu crio o objeto para comparação 
            #cmp = obj_cmp.__dict__ == obj.__dict__
            #return cmp, obj
            pass

        elif isinstance(obj, Livro):
            #Aqui eu vou checar se os dados do livros são correspondentes a algum já existente
            linha_alvo = self._df_livros[self._df_livros["nome"]==obj.nome]
            if len(linha_alvo)==0:
                return False
            #Depois se compara com a linha achada
            #obj_cmp = Livros() aqui se cria o objeto 
            # cmp = obj_cmp.__dict__ == obj.__dict__
            #return cmp, obj

            pass

        else: 
            raise ValueError("Objeto inserido desconhecido")

    def atualizar_objeto(self, obj): 
        if isinstance(obj, UsuarioComum): 
            #Procurando e recebendo o usuario pelo ID
            is_user_true = self.procurar_objeto(obj)

            if is_user_true:
                #Sobrescrever a linha deles no df
                mask = self._df_pessoas["id"] == obj.id

                for coluna in self._df_pessoas.keys():
                    self._df_pessoas.loc[mask, str(coluna)] = obj.coluna #Usando .loc para não modificar uma cópia do df

            #Escrever no CSV
            #?
            pass
        elif isinstance(obj, Livro):
            #Procurando e recebendo o usuario pelo nome do livro
            #Sobrescrever a linha dele no df
            #Escrever no CSV
            pass
        else: 
            raise ValueError("Objeto inserido desconhecido")

        return True


def test(): 
    bd1 = BDmanager()
    bd1.carregar_database()

test()