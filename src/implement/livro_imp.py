"""
Este código é a implementação da classe Livro
Aqui se implementa os atributos e métodos obrigatórios
"""
#from src.models.livro_cnt import Livro_cnt
#from src.models.usuario_comum_cnt import UsuarioComum_cnt
#from src.implement.BDManager_imp import BDmanager

# TIRAR SETTER (???)


class Livro():
    
    def __init__(self, titulo: str, autor: str, ano: int, num_paginas: int, 
                 categoria: str, editora: str, descricao: str, faixa_etaria: str):
        self.titulo = titulo # g/s OK
        self.autor = autor # g/s OK
        self.ano = ano # g/s OK
        self.num_paginas = num_paginas # g/s OK
        self.categoria = categoria # g/s OK
        self.editora = editora # g/s OK
        self.descricao = descricao # g/s OK
        self.faixa_etaria = faixa_etaria # g/s

        self.__estrelas = 3.5 #so get (atualiza a cada avaliacao)
        self.__resenhas = ["legal", "ok", "a", "b"] #so get (idem)
    
    # TITULO
    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo: str) -> None:
        if not isinstance(titulo, str): # se não for string... (not False = True)
            raise TypeError("O Titulo deve ser uma String")
        titulo_str = titulo.strip() # elimina espacos
        if not titulo_str: # se for vazio...
            raise ValueError("O Titulo não pode ser vazio.")
        self.__titulo = titulo_str

    # AUTOR
    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, autor: str) -> None:
        if not isinstance(autor, str):
            raise TypeError("O autor deve ser uma String.")
        autor_str = autor.strip()
        if not autor_str:
            raise ValueError("O Autor não pode ser vazio.")
        self.__autor = autor_str

    # ANO
    @property
    def ano(self) -> int:
        return self.__ano

    @ano.setter
    def ano(self, ano: int) -> None:
        if not isinstance(ano, int):
            raise TypeError("O ano deve ser um número inteiro")
        if ano > 2026: # pode ser negativo, considerando a.C
            raise ValueError("O ano não pode ser um ano futuro")
        self.__ano = ano

    # NUMERO DE PAGINAS
    @property
    def num_paginas(self) -> str:
        return self.__num_paginas

    @num_paginas.setter
    def num_paginas(self, num_paginas: int) -> None:
        if not isinstance(num_paginas, int):
            raise TypeError("O número de páginas deve ser um número inteiro")
        if num_paginas <= 0:
            raise ValueError("O número de páginas deve ser maior que zero")
        self.__num_paginas = num_paginas
        
    # CATEGORIA
    @property
    def categoria(self) -> str:
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria: str) -> None:
        if not isinstance(categoria, str):
            raise TypeError("A categoria deve ser uma String")
        categoria_str = categoria.strip()
        if not categoria_str:
            raise ValueError("A Categoria não pode ser vazia")
        self.__categoria = categoria_str

    # EDITORA
    @property
    def editora(self) -> str:
        return self.__editora

    @editora.setter
    def editora(self, editora: str) -> None:
        if not isinstance(editora, str):
            raise TypeError("A editora deve ser uma String!")
        editora_str = editora.strip()
        if not editora_str:
            raise ValueError("A Editora não pode ser vazia!")
        self.__editora = editora_str

    # DESCRIÇÃO
    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser uma String.")
        descricao_str = descricao.strip()
        if not descricao_str:
            raise ValueError("A descrição não pode ser vaiza.")
        self.__descricao = descricao_str

    # FAIXA ETARIA
    @property
    def faixa_etaria(self) -> str:
        return self.__faixa_etaria

    @faixa_etaria.setter
    def faixa_etaria(self, faixa_etaria: str) -> None:
        if not isinstance(faixa_etaria, str):
            raise TypeError("A Faixa Etária deve ser uma String")
        faixa_etaria_str = faixa_etaria.strip()
        if not faixa_etaria_str:
            raise ValueError("A Faixa Etária não pode ser vazia")
        self.__faixa_etaria = faixa_etaria_str

    # completamente provisório e incompleto !!!!!!
    def avaliar(self, nota: float, resenha: str) -> None:
        if nota < 0 or nota > 5:
            raise ValueError("A nota deve ser entre 0 e 5.")
        resenha_str = resenha.strip()
        if not resenha_str:
            raise ValueError("A resenha não pode ser vazia")
        qtd_avaliacoes = len(self.__resenhas)
        nota_total = qtd_avaliacoes * self.__estrelas
        media_nova = (nota_total + nota) / (qtd_avaliacoes + 1)
        
        self.__resenhas.append(resenha_str)
        self.__estrelas = media_nova
        print(f"O Livro foi avaliado com sucesso!")
        print(f"Nova média: {media_nova}") # Tirar depois

livro1 = Livro(
        titulo="harry potter",
        autor="otavio",
        ano=2000,
        num_paginas=100,
        categoria="fantasia",
        editora="abc",
        descricao="harry potter bla bla bla",
        faixa_etaria="12+"
    )

livro1.avaliar(5, "Obra prima")

'''
for i in livro1.resenhas:
    print(i)

livro1.titulo = "abc"
print(livro1.titulo)
#print(livro1.__titulo)
livro1.avaliar(4.8, "Obra prima parte 2")
for i in livro1.resenhas:
    print(i)
    '''