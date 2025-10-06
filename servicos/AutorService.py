import os
from modelos.Autor import Autor 

class AutorService:
    def __init__(self, arquivo_autores, indice_autores_global, ler_registro, 
                 percorrer_inorder, marcar_excluido, buscar_cidade):
        self.ARQUIVO = arquivo_autores
        self.indice = indice_autores_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.marcar_registro_como_excluido = marcar_excluido
        self.buscar_cidade_por_codigo = buscar_cidade 
        self.campos = ['codigo_autor', 'nome', 'codigo_cidade']

    def consultar_registro(self, codigo_consulta):
        no_encontrado = self.indice.buscar(codigo_consulta)
        
        if no_encontrado:
            registro_str = self.ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 3:
                    autor = Autor(int(dados[0]), dados[1], dados[2])
                    
                    cidade = self.buscar_cidade_por_codigo(autor.codigo_cidade)
                    
                    print("\n" + "="*40)
                    print(f"** DADOS DO AUTOR **")
                    print(f"Nome: {autor.nome} (Cód: {autor.codigo_autor})")
                    print("-" * 40)
                    
                    if cidade:
                        print(f"-> Cidade Natal: {cidade.descricao}, {cidade.estado}")
                    else:
                        print(f"-> Cidade Natal: Cód. {autor.codigo_cidade} (Não Encontrada)")
                    
                    print("=" * 40)
                    return autor
        
        print(f"Autor com código {codigo_consulta} não encontrado.")
        return None
    
    def leitura_exaustiva(self):
        print(f"\n--- Leitura Exaustiva de Autores ---")
        
        print("="*80)
        print(f"{'CÓDIGO':<10} | {'NOME DO AUTOR':<30} | {'CIDADE/ESTADO DE ORIGEM':<35}")
        print("="*80)
        contador = 0
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 3:
                    autor = Autor(int(dados[0].replace('*','')), dados[1], dados[2])
                    cidade = self.buscar_cidade_por_codigo(autor.codigo_cidade)
                    cidade_info = f"{cidade.descricao} / {cidade.estado}" if cidade else f"Cód: {autor.codigo_cidade} (Não Encontrada)"
                    
                    print(
                        f"{autor.codigo_autor:<10} | "
                        f"{autor.nome:<30} | "
                        f"{cidade_info:<35}")
                    contador += 1
        
        print("="*80)
        print(f"\nTotal de {contador} autores listados.")
        return contador
    
    def excluir_registro(self, codigo_excluir):
        posicao_do_registro = self.indice.remover(codigo_excluir) 
        
        if posicao_do_registro is not None:
            self.marcar_registro_como_excluido(posicao_do_registro, self.ARQUIVO)
            print(f"SUCESSO: Autor com código {codigo_excluir} removido logicamente.")
            return True
        
        print(f"ERRO: Autor com código {codigo_excluir} não encontrado para exclusão.")
        return False