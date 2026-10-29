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
        print(df_livros.head(n=1))
        print(df_livros.info())

        self._df_livros = df_livros
        #self.df_livros = df_pessoas
        return True
    
    def validar_objeto(self, obj) -> bool:
        if isinstance(obj, UsuarioComum): 
            #Aqui eu vou checar se o id do usuário existe no df
            pass
        elif isinstance(obj, Livro):
            #Aqui eu vou checar se os dados do livros são correspondentes a algum já existente
            pass
        else: 
            raise ValueError("Objeto inserido desconhecido")

        return True
    
    def procurar_objeto(self, obj): 
        if isinstance(obj, UsuarioComum): 
            #Aqui eu vou checar se o id do usuário existe no df e retornar ele
            pass
        elif isinstance(obj, Livro):
            #Aqui eu vou checar se os dados do livros são correspondentes a algum já existente e retornar ele
            pass
        else: 
            raise ValueError("Objeto inserido desconhecido")

        return True

    def atualizar_objeto(self, obj): 
        if isinstance(obj, UsuarioComum): 
            #Procurando e recebendo o usuario pelo ID
            is_user_true = self.procurar_objeto(obj)

            if is_user_true:
                #Sobrescrever a linha dele no df
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