from modelos.Cidade import Cidade
import os

class CidadeService:
    def __init__(self, arquivo_cidades, indice_cidades_global, ler_registro, percorrer_inorder, marcar_excluido):
        self.ARQUIVO = arquivo_cidades
        self.indice = indice_cidades_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.marcar_registro_como_excluido = marcar_excluido
        self.campos = ['codigo_cidade', 'descricao', 'estado']

    def _salvar_e_indexar(self, cidade):
        try:
            with open(self.ARQUIVO, 'a') as dados_do_arquivo:
                posicao = dados_do_arquivo.tell() 
                registro_str = ";".join(str(getattr(cidade, campo)) for campo in self.campos) + "\n"
                dados_do_arquivo.write(registro_str)
                
                codigo = getattr(cidade, self.campos[0])
                if not self.indice.buscar(codigo):
                    self.indice.inserir(codigo, posicao)
                else:
                    print(f"AVISO: Código {codigo} já existia no índice. Não inserido.")
            return True
        except Exception as e:
            print(f"ERRO ao salvar Cidade: {e}")
            return False

    def incluir_registro(self, codigo, descricao, estado):
        try:
            if self.indice.buscar(codigo):
                print(f"ERRO: Código {codigo} já existe.")
                return False
            
            nova_cidade = Cidade(codigo, descricao, estado)
            if self._salvar_e_indexar(nova_cidade):
                print(f"SUCESSO: Cidade {descricao} ({codigo}) incluída.")
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
                if len(dados) >= 3:
                    cidade = Cidade(int(dados[0]), dados[1], dados[2]) 
                    print("\n--- Dados da Cidade ---")
                    print(cidade)
                    return cidade
        print(f"Cidade com código {codigo_consulta} não encontrada.")
        return None

    def excluir_registro(self, codigo_excluir):
        posicao_do_registro = self.indice.remover(codigo_excluir)
        
        if posicao_do_registro is not None:
            self.marcar_registro_como_excluido(posicao_do_registro, self.ARQUIVO)
            print(f"SUCESSO: Cidade com código {codigo_excluir} removida logicamente.")
            return True
        print(f"ERRO: Cidade com código {codigo_excluir} não encontrada para exclusão.")
        return False

    def leitura_exaustiva(self):
        print(f"\n--- Leitura Exaustiva de Cidades ---")
        
        print("="*60)
        print(f"{'CÓDIGO':<10} | {'CIDADE':<30} | {'ESTADO':<10}")
        print("="*60)
        contador = 0
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 3:
                    cidade = Cidade(int(dados[0].replace('*','')), dados[1], dados[2])
                    
                    print(
                        f"{cidade.codigo_cidade:<10} | "
                        f"{cidade.descricao:<30} | "
                        f"{cidade.estado:<10}")
                    contador += 1
        
        print("="*60)
        print(f"\nTotal de {contador} cidades listadas.")
        return contador