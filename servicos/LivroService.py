import os
from modelos.Livro import Livro 

class LivroService:
    def __init__(self, arquivo_livros, indice_livros_global, ler_registro, 
                 percorrer_inorder, marcar_excluido, 
                 buscar_autor, buscar_categoria, buscar_cidade):
        self.ARQUIVO = arquivo_livros
        self.indice = indice_livros_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.marcar_registro_como_excluido = marcar_excluido
        
        self.buscar_autor_por_codigo = buscar_autor 
        self.buscar_categoria_por_codigo = buscar_categoria
        self.buscar_cidade_por_codigo = buscar_cidade 
        
        self.campos = ['codigo_livro', 'titulo', 'codigo_autor', 'codigo_categoria', 'ano_publicacao', 'disponibilidade']

    def _salvar_e_indexar(self, livro):
        try:
            with open(self.ARQUIVO, 'a') as dados_do_arquivo:
                posicao = dados_do_arquivo.tell() 
                registro_str = ";".join(str(getattr(livro, campo)) for campo in self.campos) + "\n"
                dados_do_arquivo.write(registro_str)
                
                codigo = getattr(livro, self.campos[0])
                if not self.indice.buscar(codigo):
                    self.indice.inserir(codigo, posicao)
                return True
        except Exception as e:
            print(f"ERRO ao salvar Livro: {e}")
            return False

    def incluir_registro(self):
        print("\n--- Inclusão de Novo Livro ---")
        
        while True:
            try:
                codigo = int(input("Código do Livro: "))
                if self.indice.buscar(codigo):
                    print(f"ERRO: Código {codigo} já existe.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")

        titulo = input("Título do Livro: ")
        cod_autor = input("Código do Autor: ")
        cod_categoria = input("Código da Categoria: ")
        ano_publicacao = input("Ano de Publicação: ")

        if not self.buscar_autor_por_codigo(cod_autor):
            print(f"ERRO: Autor com código {cod_autor} não encontrado. Inclusão cancelada.")
            return False
            
        if not self.buscar_categoria_por_codigo(cod_categoria):
            print(f"ERRO: Categoria com código {cod_categoria} não encontrada. Inclusão cancelada.")
            return False
        
        novo_livro = Livro(codigo, titulo, cod_autor, cod_categoria, ano_publicacao, "disponivel")
        
        if self._salvar_e_indexar(novo_livro):
            print(f"SUCESSO: Livro '{titulo}' incluído com status 'disponivel'.")
            return True
        return False

    def consultar_registro(self, codigo_consulta):
        """ Consulta um Livro e realiza JOIN com Autor e Categoria. """
        livro = self.consultar_registro_simples(codigo_consulta)
        
        if livro:
            categoria = self.buscar_categoria_por_codigo(livro.cod_categoria)
            
            autor = self.buscar_autor_por_codigo(livro.cod_autor)
            
            cidade_autor = self.buscar_cidade_por_codigo(autor.codigo_cidade) if autor else None

            print("\n" + "="*50)
            print(f"** LIVRO: {livro.titulo} (Cód: {livro.codigo_livro}) **")
            print("="*50)
            print(f"-> Publicação: {livro.ano_publicacao}")
            print(f"-> Status: {livro.disponibilidade.upper()} (Item 4.3)")
            
            cat_info = categoria.descricao if categoria else f"Cód: {livro.cod_categoria} (Não encontrado)"
            print(f"-> Categoria: {cat_info}")
            
            if autor:
                print(f"-> Autor: {autor.nome} (Cód: {livro.cod_autor})")
                cidade_info = f"{cidade_autor.descricao}, {cidade_autor.estado}" if cidade_autor else "Não Informada"
                print(f"   -> Cidade Natal: {cidade_info}") 
            else:
                print(f"-> Autor: Cód: {livro.cod_autor} (Não encontrado)")
            
            print("=" * 50)
            return livro
        
        print(f"Livro com código {codigo_consulta} não encontrado.")
        return None
        
    def consultar_registro_simples(self, codigo_consulta):
        try:
            codigo_int = int(codigo_consulta)
        except ValueError:
            return None
        
        no_encontrado = self.indice.buscar(codigo_int)
        
        if no_encontrado:
            registro_str = self.ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= len(self.campos):
                    return Livro(int(dados[0]), dados[1], dados[2], dados[3], dados[4], dados[5])
        return None


    def excluir_registro(self, codigo_excluir):
        posicao_do_registro = self.indice.remover(codigo_excluir)
        
        if posicao_do_registro is not None:
            self.marcar_registro_como_excluido(posicao_do_registro, self.ARQUIVO)
            print(f"SUCESSO: Livro com código {codigo_excluir} removido logicamente.")
            return True
        
        print(f"ERRO: Livro com código {codigo_excluir} não encontrado para exclusão.")
        return False

    def leitura_exaustiva(self):
        print(f"\n--- Leitura Exaustiva de Livros (Ordem Crescente de Código) ---")
        
        total_disponivel = 0
        total_emprestado = 0

        print("="*100)
        print(f"{'CÓDIGO':<6} | {'TÍTULO':<20} | {'AUTOR':<15} | {'CATEGORIA':<15} | {'STATUS':<10}")
        print("="*100)
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= len(self.campos):
                    livro = Livro(int(dados[0].replace('*','')), dados[1], dados[2], dados[3], dados[4], dados[5])
                    
                    autor = self.buscar_autor_por_codigo(livro.codigo_autor)
                    categoria = self.buscar_categoria_por_codigo(livro.codigo_categoria)
                    
                    if livro.disponibilidade.lower() == 'disponivel':
                        total_disponivel += 1
                    else:
                        total_emprestado += 1
                        
                    autor_nome = autor.nome if autor else f"Cód:{livro.codigo_autor}"
                    categoria_nome = categoria.descricao if categoria else f"Cód:{livro.codigo_categoria}"
                    titulo_curto = livro.titulo[:40] 
                    
                    print(
                        f"{livro.codigo_livro:<6} | "
                        f"{titulo_curto:<20} | "
                        f"{autor_nome:<15} | "
                        f"{categoria_nome:<15} | "
                        f"{livro.disponibilidade.upper():<10}"
                    )

        print("="*100)
        print("\n" + "="*80)
        print(f"RELATÓRIO DE STATUS DE LIVROS")
        print(f"Quantidade de livros DISPONÍVEIS: {total_disponivel}")
        print(f"Quantidade total de livros EMPRESTADOS: {total_emprestado}")
        print("="*80)
        return total_disponivel, total_emprestado
    
    def atualizar_disponibilidade(self, codigo_livro, novo_status):
        try:
            codigo_int = int(codigo_livro)
        except ValueError:
            return False

        no = self.indice.buscar(codigo_int)
        
        if no:
            posicao = no.posicao_no_arquivo
            
            registro_str = self.ler_registro_no_arquivo(posicao, self.ARQUIVO)
            if not registro_str or registro_str.startswith('*'):
                print("ERRO: Registro do livro não pôde ser lido ou está excluído.")
                return False

            dados = registro_str.split(';')
            
            if len(dados) > 5: 
                dados[5] = novo_status 
            else:
                print("ERRO: O registro do livro não tem o número esperado de campos.")
                return False
                
            nova_linha = ";".join(dados) + "\n"
            
            try:
                with open(self.ARQUIVO, 'r+') as f:
                    f.seek(posicao)
                    f.write(nova_linha) 
                return True
            except Exception as e:
                print(f"ERRO ao reescrever registro do livro: {e}")
                return False
        return False