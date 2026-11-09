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
        # TITULO
        if not isinstance(titulo, str): # se não for string... (not False = True)
            raise TypeError("O Titulo deve ser uma String")
        titulo = titulo.strip() # elimina espacos
        if not titulo: # se for vazio...
            raise ValueError("O Titulo não pode ser vazio.")

        # AUTOR
        if not isinstance(autor, str):
            raise TypeError("O autor deve ser uma String.")
        autor = autor.strip()
        if not autor:
            raise ValueError("O Autor não pode ser vazio.")

        # ANO
        if not isinstance(ano, int):
            raise TypeError("O ano deve ser um número inteiro")
        if ano > 2026: # pode ser negativo, considerando a.C
            raise ValueError("O ano não pode ser um ano futuro")
        
        # NUMERO DE PAGINAS
        if not isinstance(num_paginas, int):
            raise TypeError("O número de páginas deve ser um número inteiro")
        if num_paginas <= 0:
            raise ValueError("O número de páginas deve ser maior que zero")     

        # CATEGORIA
        if not isinstance(categoria, str):
            raise TypeError("A categoria deve ser uma String")
        categoria = categoria.strip()
        if not categoria:
            raise ValueError("A Categoria não pode ser vazia")

        # EDITORA
        if not isinstance(editora, str):
            raise TypeError("A editora deve ser uma String!")
        editora = editora.strip()
        if not editora:
            raise ValueError("A Editora não pode ser vazia!")

        # DESCRICAO
        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser uma String.")
        descricao = descricao.strip()
        if not descricao:
            raise ValueError("A descrição não pode ser vaiza.")

        # FAIXA ETARIA
        if not isinstance(faixa_etaria, str):
            raise TypeError("A Faixa Etária deve ser uma String")
        faixa_etaria = faixa_etaria.strip()
        if not faixa_etaria:
            raise ValueError("A Faixa Etária não pode ser vazia")
        
               
        self._titulo = titulo # g OK
        self._autor = autor # g OK
        self._ano = ano # g OK
        self._num_paginas = num_paginas # g OK
        self._categoria = categoria # g OK
        self._editora = editora # g OK
        self._descricao = descricao # g OK
        self._faixa_etaria = faixa_etaria # g OK

        # valores testes (zerar dps)
        self._estrelas = 0.0 #so get (atualiza a cada avaliacao)
        self._resenhas = [] #so get (idem)
    
    # TITULO
    @property
    def titulo(self) -> str:
        return self._titulo
 
    # AUTOR
    @property
    def autor(self) -> str:
        return self._autor

    # ANO
    @property
    def ano(self) -> int:
        return self._ano

    # NUMERO DE PAGINAS
    @property
    def num_paginas(self) -> int:
        return self._num_paginas
        
    # CATEGORIA
    @property
    def categoria(self) -> str:
        return self._categoria

    # EDITORA
    @property
    def editora(self) -> str:
        return self._editora
    
    # DESCRIÇÃO
    @property
    def descricao(self) -> str:
        return self._descricao

    # FAIXA ETARIA
    @property
    def faixa_etaria(self) -> str:
        return self._faixa_etaria

    # ESTRELAS
    @property
    def estrelas(self) -> float:
        return self._estrelas

    # RESENHAS
    @property
    def resenhas(self) -> list[str]:
        return self._resenhas

    # completamente provisório e incompleto !!!!!!
    def avaliar(self, nota: float, resenha: str) -> None:
        if nota < 0 or nota > 5:
            raise ValueError("A nota deve ser entre 0 e 5.")
        resenha_str = resenha.strip()
        if not resenha_str:
            raise ValueError("A resenha não pode ser vazia")
        qtd_avaliacoes = len(self.__resenhas)
        nota_total = qtd_avaliacoes * self._estrelas
        media_nova = (nota_total + nota) / (qtd_avaliacoes + 1)
        
        self._resenhas.append(resenha_str)
        self._estrelas = media_nova
        print(f"O Livro foi avaliado com sucesso!")
        print(f"Nova média: {media_nova}") # Tirar depois

# apenas para teste (remover)
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
"""
livro1.avaliar(5, "Obra prima")
livro1.__autor = "abc"
print(livro1.autor)
"""
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