"""
Este código é a implementação da classe BDmanager.
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.clube_livro_cnt import ClubeLivro_cnt
from src.implement.livro_imp import Livro
from src.implement.usuario_gerente_imp import UsuarioGerente

from pathlib import Path
import pandas as pd, json 
import json

class ClubeLivro(ClubeLivro_cnt):
    def __init__(self, moderador:UsuarioGerente):
        self.__nome_clube = ""
        self.__livros = []
        self.__membros = []
        self.__excluidos = []
        self.__moderador = [moderador.login]

    @property
    def moderador(self) -> list:
        return self.__moderador

    @property
    def livros(self) -> list:
        return self.__livros

    @property
    def membros(self) -> list:
        return self.__membros

    @property
    def nome(self):
        return self.__nome_clube

    def definir_nome(self, solicitante:UsuarioGerente, nome):
        if self.__moderador[0] == solicitante.login: 
            self.__nome_clube = nome
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")
            
    def process_list(self,lista) -> list:
        lista_proces = []

        for i in range(1, len(lista), 2):
            lista_proces.append(lista[i])
        return lista_proces

    def carregar_dados(self):
        with open("src/database/Teste.txt", mode='r+') as f:
            
            dados_totais = f.readlines()
            
            if len(dados_totais)==0: 
                print("Database vazia")
                return False
            f.seek(0)
            try:
                listas = []
                for linha in f:
                    
                    listas.append( linha.strip().split("'"))
                listas_processadas = []
                for lista in listas:
                    listas_processadas.append(self.process_list(lista))
                
            except Exception as e:
                raise ValueError("Problema na base de dados do clube do livro")
            
        self.__moderador , self.__membros, self.__excluidos, self.__livros = listas_processadas
        return True

    def salvar_dados(self):
        if  len(self.__membros)==0 or len(self.__livros)==0 or len(self.__moderador)==0:
            raise ValueError("Há atributos nulos sendo salvos, preencha todas as informações básicas antes")
        with open("src/database/Teste.txt", mode='a+') as f:
            try:
                f.write(str(self.__moderador))
                f.write("\n")
                f.write(str(self.__membros))
                f.write("\n")
                if len(self.__excluidos)==0:
                    f.write("[""]")
                    f.write("\n")
                else:
                    f.write(str(self.__excluidos))
                    f.write("\n")
                f.write(str(self.__livros))
                f.write("\n")
            except Exception as e:
                raise ValueError("Problema ao salvar na base de dados do clube do livro")

    def adicionar_livro(self, solicitante:UsuarioGerente, Livro:Livro):
        if self.__moderador[0] == solicitante.login: 
           self.__livros.append(Livro.titulo)
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")
               
    def adicionar_pessoa(self, solicitante:UsuarioGerente, adicionado):
        if self.__moderador[0] == solicitante.login:
            if adicionado.login in self.__excluidos:
                print("Membro já foi excluido anteriormente!")
                return
            self.__membros.append(adicionado.login) #Qual atributo do adicionado salvar ?
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")

    def expulsar_pessoa(self, solicitante:UsuarioGerente, expulso):
        if self.__moderador[0] == solicitante.login: 
            idx = self.__membros.index(expulso.login)# Já gera erro no caso de membro indisponível
            self.__excluidos.append(self.__membros[idx])
            self.__membros.pop(idx) #Qual atributo do adicionado salvar ?
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")

    def redefinir_moderador(self, solicitante:UsuarioGerente, novo_mod:UsuarioGerente):
        if self.__moderador[0] == solicitante.login: 
            self.__moderador[0]=novo_mod.login
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")

    def ver_expulsos(self, solicitante:UsuarioGerente) -> list:
        if self.__moderador[0] == solicitante.login: 
            return self.__excluidos
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")

def test(): 
    p1 = UsuarioGerente("ze", "pedro", "abc123")
    c1 = ClubeLivro(p1)
    c1.carregar_dados()
    print(c1.membros,c1.moderador, c1.livros)
    print("Expulsos: ",c1.ver_expulsos(p1), len(c1.ver_expulsos(p1)))

    l1 = Livro("A Sombra no Porão","Marcos Valadares", 2018,312,"terror","Editora Noite Alta","Uma família descobre que o porão da casa nova guarda algo que se alimenta do medo.","16+")
    l2 = Livro("Ze maria","Marcos Valadares", 2018,312,"terror","Editora Noite Alta","Uma família descobre que o porão da casa nova guarda algo que se alimenta do medo.","16+")
    c1.adicionar_livro(p1, l1)
    c1.adicionar_livro(p1, l2)

    p2 = UsuarioGerente("ze", "bist", "abc123")
    p3 = UsuarioGerente("ze", "bisteca", "abc123")
    c1.adicionar_pessoa(p1, p2) 
    c1.adicionar_pessoa(p1, p3)
    print("ANTES: ",c1.membros,c1.moderador, c1.livros)
    print("Expulsos: ",c1.ver_expulsos(p1))

    c1.expulsar_pessoa(p1, p2)
    c1.adicionar_pessoa(p1, p2)
    #c1.salvar_dados()
    print("DEPOIS: ",c1.membros,c1.moderador, c1.livros)
    print("Expulsos: ",c1.ver_expulsos(p1))

    """
    p2 = UsuarioComum("ze", "bist", "abc123")
    p3 = UsuarioComum("ze", "bisteca", "abc123")

    c1.adicionar_pessoa(p1, p2) (Validado)
    c1.adicionar_pessoa(p1, p3) (Validado)
    c1.salvar_dados() ( xcluidos)
    """
    
    
    

test()