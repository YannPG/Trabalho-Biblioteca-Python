import os
from modelos.Aluno import Aluno 

class AlunoService:
    def __init__(self, arquivo_alunos, indice_alunos_global, ler_registro, 
                 percorrer_inorder, buscar_curso, buscar_cidade, marcar_excluido):
        self.ARQUIVO_ALUNOS = arquivo_alunos
        self.indice_alunos = indice_alunos_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.buscar_curso_por_codigo = buscar_curso
        self.buscar_cidade_por_codigo = buscar_cidade
        self.marcar_registro_como_excluido = marcar_excluido
        
    def salvar_aluno_no_arquivo(self, aluno):
        with open(self.ARQUIVO_ALUNOS, 'a') as dados_do_arquivo:
            posicao_registro = dados_do_arquivo.tell() 
            registro_str = f"{aluno.codigo_aluno};{aluno.nome};{aluno.codigo_curso};{aluno.codigo_cidade}\n"
            dados_do_arquivo.write(registro_str)
            return posicao_registro

    def incluir_aluno(self):
        print("\n--- Inclusão de Novo Aluno ---")
        while True:
            try:
                codigo = int(input("Digite o Código do Aluno (apenas números): "))
                if self.indice_alunos.buscar(codigo):
                    print(f"O código {codigo} já existe. Tente outro.")
                else:
                    break
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")

        nome = input("Nome do Aluno: ")
        codigo_curso = input("Código do Curso: ")
        codigo_cidade = input("Código da Cidade: ")
        
        novo_aluno = Aluno(codigo, nome, codigo_curso, codigo_cidade)
        posicao = self.salvar_aluno_no_arquivo(novo_aluno)
        
        self.indice_alunos.inserir(codigo, posicao)
        print(f"\nSUCESSO: Aluno '{nome}' incluído. Posição no arquivo: {posicao}")

    def consultar_aluno(self, codigo_consulta):
        no_aluno = self.indice_alunos.buscar(codigo_consulta)
        
        if no_aluno:
            posicao = no_aluno.posicao_no_arquivo
            registro_str = self.ler_registro_no_arquivo(posicao, self.ARQUIVO_ALUNOS)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 4:
                    aluno = Aluno(int(dados[0]), dados[1], dados[2], dados[3])
                    
                    curso = self.buscar_curso_por_codigo(aluno.codigo_curso)
                    cidade = self.buscar_cidade_por_codigo(aluno.codigo_cidade)
                    
                    print("\n" + "="*40)
                    print(f"** DADOS DO ALUNO **")
                    print(f"Nome: {aluno.nome} (Cód: {aluno.codigo_aluno}) ")
                    print("-" * 40)
                    
                    curso_info = f"{curso.descricao}" if curso else "Não Encontrado"
                    print(f"Curso: {curso_info} (Cód: {aluno.codigo_curso})")

                    cidade_info = f"{cidade.descricao} / {cidade.estado}" if cidade else "Não Encontrada"
                    print(f"Cidade: {cidade_info} (Cód: {aluno.codigo_cidade})")
                    
                    print("=" * 40)
                else:
                    print(f"ERRO: Formato de registro inválido para o código {codigo_consulta}.")
        else:
            print(f"Aluno com código {codigo_consulta} não encontrado no sistema.")

    def consultar_registro_simples(self, codigo_consulta):
        try:
            codigo_int = int(codigo_consulta)
        except ValueError:
            return None
            
        no_aluno = self.indice_alunos.buscar(codigo_int)
        
        if no_aluno:
            posicao = no_aluno.posicao_no_arquivo
            registro_str = self.ler_registro_no_arquivo(posicao, self.ARQUIVO_ALUNOS)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 4:
                    return Aluno(int(dados[0]), dados[1], dados[2], dados[3])
        return None

    def excluir_aluno(self, codigo_excluir):
        posicao_do_registro = self.indice_alunos.remover(codigo_excluir)
        
        if posicao_do_registro is not None:
            self.marcar_registro_como_excluido(posicao_do_registro, self.ARQUIVO_ALUNOS)
            print(f"\nSUCESSO: Aluno com código {codigo_excluir} foi removido do índice.")
        else:
            print(f"Aluno com código {codigo_excluir} não encontrado para exclusão.")        

    def leitura_exaustiva(self):
        print(f"\n--- Leitura Exaustiva de Alunos ---")
        
        print("="*100)
        print(f"{'CÓDIGO':<6} | {'NOME DO ALUNO':<30} | {'CURSO':<35} | {'CIDADE/ESTADO':<20}")
        print("="*100)
        contador = 0
        
        for no in self.percorrer_inorder(self.indice_alunos.raiz):
            posicao = no.posicao_no_arquivo
            registro_str = self.ler_registro_no_arquivo(posicao, self.ARQUIVO_ALUNOS)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 4:
                    aluno = Aluno(
                        codigo_aluno=int(dados[0].replace('*','')), 
                        nome=dados[1],
                        codigo_curso=dados[2],
                        codigo_cidade=dados[3]
                    )
                    
                    curso = self.buscar_curso_por_codigo(aluno.codigo_curso)
                    cidade = self.buscar_cidade_por_codigo(aluno.codigo_cidade)
                    curso_info = curso.descricao if curso else f"Cód: {aluno.codigo_curso}"
                    cidade_info = f"{cidade.descricao}/{cidade.estado}" if cidade else f"Cód: {aluno.codigo_cidade}"
                    
                    print(
                        f"{aluno.codigo_aluno:<6} | "
                        f"{aluno.nome:<30} | "
                        f"{curso_info:<35} | "
                        f"{cidade_info:<20}")
                    contador += 1
        
        print("="*100)
        print(f"\nTotal de {contador} alunos listados.")
        return contador
