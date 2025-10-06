import os
from modelos.Curso import Curso

class CursoService:
    def __init__(self, arquivo_cursos, indice_cursos_global, ler_registro, percorrer_inorder, marcar_excluido):
        self.ARQUIVO = arquivo_cursos
        self.indice = indice_cursos_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.marcar_registro_como_excluido = marcar_excluido
        self.campos = ['codigo_curso', 'descricao']

    def _salvar_e_indexar(self, curso):
        try:
            with open(self.ARQUIVO, 'a') as dados_do_arquivo:
                posicao = dados_do_arquivo.tell() 
                registro_str = ";".join(str(getattr(curso, campo)) for campo in self.campos) + "\n"
                dados_do_arquivo.write(registro_str)
                
                codigo = getattr(curso, self.campos[0])
                if not self.indice.buscar(codigo):
                    self.indice.inserir(codigo, posicao)
                else:
                    print(f"AVISO: Código {codigo} já existia no índice. Não inserido.")
            return True
        except Exception as e:
            print(f"ERRO ao salvar Curso: {e}")
            return False

    def incluir_registro(self, codigo, descricao):
        try:
            if self.indice.buscar(codigo):
                print(f"ERRO: Código {codigo} já existe.")
                return False
            
            novo_curso = Curso(codigo, descricao)
            if self._salvar_e_indexar(novo_curso):
                print(f"SUCESSO: Curso {descricao} ({codigo}) incluído.")
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
                    curso = Curso(int(dados[0]), dados[1]) 
                    print("\n--- Dados do Curso ---")
                    print(curso)
                    return curso
        print(f"Curso com código {codigo_consulta} não encontrado.")
        return None

    def excluir_registro(self, codigo_excluir):
        posicao_do_registro = self.indice.remover(codigo_excluir)
        
        if posicao_do_registro is not None:
            self.marcar_registro_como_excluido(posicao_do_registro, self.ARQUIVO)
            print(f"SUCESSO: Curso com código {codigo_excluir} removido logicamente.")
            return True
        print(f"ERRO: Curso com código {codigo_excluir} não encontrado para exclusão.")
        return False

    def leitura_exaustiva(self):
        print(f"\n--- Leitura Exaustiva de Cursos ---")
        
        print("="*50)
        print(f"{'CÓDIGO':<10} | {'DESCRIÇÃO DO CURSO':<35}")
        print("="*50)
        contador = 0
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 2:
                    curso = Curso(int(dados[0].replace('*','')), dados[1])
                    print(
                        f"{curso.codigo_curso:<10} | "
                        f"{curso.descricao:<35}")
                    contador += 1
        
        print("="*50)
        print(f"\nTotal de {contador} cursos listados.")
        return contador