"""
Este código é a implementação da classe BDmanager.
Aqui se implementa os atributos e métodos obrigatórios
"""
from src.models.clube_livro_cnt import ClubeLivro_cnt
from src.implement.livro_imp import Livro
from src.implement.usuario_comum_imp import UsuarioComum

from pathlib import Path
import pandas as pd, json
import json

class ClubeLivro(ClubeLivro_cnt):
    def __init__(self, moderador):
        self.__livros = []
        self.__membros = []
        self.__excluidos = []
        self.__moderador = [moderador]

    @property
    def moderador(self):
        return self.__moderador

    @property
    def livros(self):
        return self.__livros

    @property
    def membros(self):
        return self.__membros

    def process_list(self,lista) -> list:
        lista_proces = []
        for i in range(1, len(lista), 2):
            lista_proces.append(lista[i])
        return lista_proces

    def carregar_dados(self):
        with open("src/database/Teste.txt", mode='r+') as f:
            listas = []
            try:
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
        with open("src/database/Teste.txt", mode='a+') as f:
            try:
                f.write(str(self.__moderador))
                f.write("\n")
                f.write(str(self.__membros))
                f.write("\n")
                f.write(str(self.__excluidos))
                f.write("\n")
                f.write(str(self.__livros))
                f.write("\n")
            except Exception as e:
                raise ValueError("Problema ao salvar na base de dados do clube do livro")

    def adicionar_livro(self, Livro:Livro):
        
        self.__livros.append(Livro.titulo)
        
    def adicionar_pessoa(self, solicitante, adicionado):
        if self.__moderador[0].id == solicitante.id: 
            self.__membros.append(adicionado) #Qual atributo do adicionado salvar ?
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")

    def expulsar_pessoa(self, solicitante, expulso):
        if self.__moderador[0].id == solicitante.id: 
            idx = self.__membros.index(solicitante)# Já gera erro no caso de membro indisponível
            self.__excluidos.append(self.__membros[idx])
            self.__membros.pop(idx) #Qual atributo do adicionado salvar ?
        else: 
            raise TypeError("Solicitante não tem autorização para realiza a operação")

    def redefinir_moderador(self, solicitante, novo_mod):
        if self.__moderador[0].id == solicitante.id: 
            self.__moderador[0]==novo_mod
        else: 
    
            raise TypeError("Solicitante não tem autorização para realiza a operação")



def test(): 
    c1 = ClubeLivro('Pedro')

    c1.salvar_dados()
    print(c1.membros, c1.moderador, c1.livros)
    
    

test()