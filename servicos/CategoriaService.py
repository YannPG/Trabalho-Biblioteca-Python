
import os
from modelos.Categoria import Categoria

class CategoriaService:
    def __init__(self, arquivo_categorias, indice_categorias_global, ler_registro, percorrer_inorder, marcar_excluido):
        self.ARQUIVO = arquivo_categorias
        self.indice = indice_categorias_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.marcar_registro_como_excluido = marcar_excluido
        self.campos = ['codigo_categoria', 'descricao']

    def _salvar_e_indexar(self, categoria):
        try:
            with open(self.ARQUIVO, 'a') as dados_do_arquivo:
                posicao = dados_do_arquivo.tell() 
                registro_str = ";".join(str(getattr(categoria, campo)) for campo in self.campos) + "\n"
                dados_do_arquivo.write(registro_str)
                
                codigo = getattr(categoria, self.campos[0])
                if not self.indice.buscar(codigo):
                    self.indice.inserir(codigo, posicao)
                else:
                    print(f"AVISO: Código {codigo} já existia no índice. Não inserido.")
            return True
        except Exception as e:
            print(f"ERRO ao salvar Categoria: {e}")
            return False

    def incluir_registro(self, codigo, descricao):
        try:
            if self.indice.buscar(codigo):
                print(f"ERRO: Código {codigo} já existe.")
                return False
            
            nova_categoria = Categoria(codigo, descricao) 
            if self._salvar_e_indexar(nova_categoria):
                print(f"SUCESSO: Categoria '{descricao}' ({codigo}) incluída.")
                return True
            return False
        except Exception:
            print("Erro na inclusão. Verifique os tipos de dados.")
            return False

    def consultar_registro(self, codigo_consulta):
        no_encontrado = self.indice.buscar(codigo_consulta)
        if no_encontrado:
            registro_str = self.ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, self.ARQUIVO)
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 2:
                    categoria = Categoria(int(dados[0]), dados[1]) 
                    print("\n--- Dados da Categoria ---")
                    print(categoria)
                    return categoria
        print(f"Categoria com código {codigo_consulta} não encontrada.")
        return None

    def excluir_registro(self, codigo_excluir):
        posicao_do_registro = self.indice.remover(codigo_excluir)
        
        if posicao_do_registro is not None:
            self.marcar_registro_como_excluido(posicao_do_registro, self.ARQUIVO)
            print(f"SUCESSO: Categoria com código {codigo_excluir} removida logicamente.")
            return True
        print(f"ERRO: Categoria com código {codigo_excluir} não encontrada para exclusão.")
        return False

    def leitura_exaustiva(self):
        print(f"\n--- Leitura Exaustiva de Categorias ---")
        
        print("="*50)
        print(f"{'CÓDIGO':<10} | {'DESCRIÇÃO DA CATEGORIA':<35}")
        print("="*50)
        contador = 0
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 2:
                    categoria = Categoria(int(dados[0].replace('*','')), dados[1])
                    
                    print(
                        f"{categoria.codigo_categoria:<10} | "
                        f"{categoria.descricao:<35}")
                    contador += 1
        
        print("="*50)
        print(f"\nTotal de {contador} categorias listadas.")
        return contador