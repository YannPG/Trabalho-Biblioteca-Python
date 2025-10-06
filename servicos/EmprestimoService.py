import os
from modelos.Emprestimo import Emprestimo
from datetime import datetime, timedelta

class EmprestimoService:
    def __init__(self, arquivo_emprestimos, indice_emprestimos_global, ler_registro, 
                 percorrer_inorder, marcar_excluido, 
                 livro_service_obj, aluno_service_obj):
        self.ARQUIVO = arquivo_emprestimos
        self.indice = indice_emprestimos_global
        self.ler_registro_no_arquivo = ler_registro
        self.percorrer_inorder = percorrer_inorder
        self.marcar_registro_como_excluido = marcar_excluido
        
        self.livro_service = livro_service_obj 
        self.aluno_service = aluno_service_obj 
        
        self.campos = ['codigo_emprestimo', 'codigo_livro', 'codigo_aluno', 'data_emprestimo', 'data_devolucao', 'devolvido']

    def _salvar_e_indexar(self, emprestimo):
        try:
            with open(self.ARQUIVO, 'a') as dados_do_arquivo:
                posicao = dados_do_arquivo.tell() 
                registro_str = ";".join(str(getattr(emprestimo, campo)) for campo in self.campos) + "\n"
                dados_do_arquivo.write(registro_str)
                
                codigo = getattr(emprestimo, self.campos[0])
                if not self.indice.buscar(codigo):
                    self.indice.inserir(codigo, posicao)
                return True
        except Exception as e:
            print(f"ERRO ao salvar Empréstimo: {e}")
            return False

    def realizar_emprestimo(self):
        print("\n--- Novo Empréstimo ---")
        codigo_emprestimo_str = input("Digite o Cód. do Empréstimo: ")
        
        try:
            codigo_emprestimo = int(codigo_emprestimo_str) 
        except ValueError:
            print("ERRO: O código do empréstimo deve ser um número inteiro.")
            return False

        codigo_livro = input("Digite o Cód. do Livro: ")
        
        livro = self.livro_service.consultar_registro_simples(codigo_livro) 
        
        if not livro:
            print(f"ERRO: Livro com código {codigo_livro} não encontrado.")
            return False
            
        if livro.disponibilidade != 'disponivel':
            print(f"ERRO: Livro '{livro.titulo}' não está disponível para empréstimo.")
            return False

        codigo_aluno = input("Digite o Cód. do Aluno: ")
        aluno = self.aluno_service.consultar_registro_simples(codigo_aluno)
        
        if not aluno:
            print(f"ERRO: Aluno com código {codigo_aluno} não encontrado.")
            return False
            
        data_emprestimo = datetime.now().strftime('%d/%m/%Y')
        data_devolucao_obj = datetime.now() + timedelta(days=7)
        data_devolucao = data_devolucao_obj.strftime('%d/%m/%Y')

        confirmar = input("Confirmar empréstimo (S/N)? ").upper() 
        
        if confirmar == 'S':
            novo_emprestimo = Emprestimo(codigo_emprestimo, codigo_livro, codigo_aluno, 
                                         data_emprestimo, data_devolucao, "Nao")
            
            if self._salvar_e_indexar(novo_emprestimo):
                self.livro_service.atualizar_disponibilidade(livro.codigo_livro, "emprestado")
                print("\nSUCESSO: Empréstimo registrado e Livro marcado como 'emprestado'.")
                return True
        
        print("Empréstimo cancelado.")
        return False
        
    def realizar_devolucao(self):
        print("\n--- Devolução de Livro ---")
        
        codigo_livro = input("Digite o Cód. do Livro a ser devolvido: ")
        
        emprestimo_ativo = self.buscar_emprestimo_ativo(codigo_livro)
        
        if not emprestimo_ativo:
            print(f"ERRO: Não foi encontrado um empréstimo ATIVO para o livro {codigo_livro}.")
            return False

        try:
            data_devolucao_prevista = datetime.strptime(emprestimo_ativo.data_devolucao, '%d/%m/%Y')
            data_atual = datetime.now()
        except ValueError:
            print("AVISO: Data de devolução inválida no registro. Não foi possível verificar atraso.")
            data_devolucao_prevista = data_atual + timedelta(days=1)
            
        if data_atual > data_devolucao_prevista:
            dias_atraso = (data_atual - data_devolucao_prevista).days
            print(f"\nAVISO: O livro está ATRASADO! ({dias_atraso} dias de atraso")
        else:
            print("Status: Dentro do prazo de devolução.")

        confirmar = input("Confirmar devolução (S/N)? ").upper()
        
        if confirmar == 'S':
            if self.atualizar_status_emprestimo(emprestimo_ativo.codigo_emprestimo, "Sim"):
                
                self.livro_service.atualizar_disponibilidade(emprestimo_ativo.codigo_livro, "disponivel")
                
                print("\nSUCESSO: Devolução registrada e Livro marcado como 'disponível'.")
                return True
            else:
                 print("ERRO: Falha ao atualizar o registro de empréstimo. Devolução não concluída.")
        
        print("Devolução cancelada.")
        return False

    def _obter_posicao_pelo_codigo(self, codigo_emprestimo):
        try:
            no = self.indice.buscar(int(codigo_emprestimo))
            return no.posicao_no_arquivo if no else None
        except ValueError:
            return None

    def atualizar_status_emprestimo(self, codigo_emprestimo, novo_status):
        posicao = self._obter_posicao_pelo_codigo(codigo_emprestimo)
        
        if posicao is None:
            return False
            
        registro_str = self.ler_registro_no_arquivo(posicao, self.ARQUIVO)
        if not registro_str or registro_str.startswith('*'):
            return False

        dados = registro_str.split(';')
        
        dados[5] = novo_status 
        nova_linha = ";".join(dados) + "\n"
        
        try:
            with open(self.ARQUIVO, 'r+') as f:
                f.seek(posicao)
                f.write(nova_linha) 
            return True
        except Exception as e:
            print(f"ERRO ao reescrever registro de empréstimo: {e}")
            return False

    def buscar_emprestimo_ativo(self, codigo_livro):
        emprestimos_do_livro = []
        
        try:
            with open(self.ARQUIVO, 'r') as f:
                for linha in f:
                    if linha.strip() and not linha.startswith('*'):
                        dados = linha.strip().split(';')
                        if len(dados) >= 6 and dados[1] == codigo_livro and dados[5].upper().startswith("N"):
                            emprestimos_do_livro.append(Emprestimo(*dados))
        except FileNotFoundError:
            return None
            
        return emprestimos_do_livro[-1] if emprestimos_do_livro else None

    def listar_emprestados(self):
        print("\n--- Relatório: Livros Atualmente Emprestados ---")
        
        print("="*100)
        print(f"{'LIVRO':<35} | {'ALUNO':<25} | {'DATA EMPR.':<12} | {'DEVOL. PREV.':<15}")
        print("="*100)
        contador = 0
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 6 and dados[5].upper().startswith("N"): 
                    emprestimo = Emprestimo(*dados)
                    
                    livro = self.livro_service.consultar_registro_simples(emprestimo.codigo_livro)
                    aluno = self.aluno_service.consultar_registro_simples(emprestimo.codigo_aluno)
                    
                    livro_titulo = livro.titulo if livro else "Livro Desconhecido"
                    aluno_nome = aluno.nome if aluno else "Aluno Desconhecido"
                    
                    print(
                        f"{livro_titulo:<35} | "
                        f"{aluno_nome:<25} | "
                        f"{emprestimo.data_emprestimo:<12} | "
                        f"{emprestimo.data_devolucao:<15}")
                    contador += 1
        
        print("="*100)
        print(f"\nTotal de {contador} livros atualmente emprestados.")

    def listar_atrasados(self):
        print("\n--- Relatório: Livros com Devolução Atrasada ---")
        
        print("="*100)
        print(f"{'LIVRO':<35} | {'ALUNO':<25} | {'DIAS ATRASO':<12} | {'DEVOL. PREV.':<15}")
        print("="*100)
        contador = 0
        data_atual = datetime.now()
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 6 and dados[5].upper().startswith("N"):
                    emprestimo = Emprestimo(*dados)
                    
                    try:
                        data_prevista = datetime.strptime(emprestimo.data_devolucao, '%d/%m/%Y')
                        
                        if data_atual > data_prevista:
                            dias_atraso = (data_atual - data_prevista).days
                            
                            livro = self.livro_service.consultar_registro_simples(emprestimo.codigo_livro)
                            aluno = self.aluno_service.consultar_registro_simples(emprestimo.codigo_aluno)

                            livro_titulo = livro.titulo if livro else "Livro Desconhecido"
                            aluno_nome = aluno.nome if aluno else "Aluno Desconhecido"

                            print(
                                f"{livro_titulo:<35} | "
                                f"{aluno_nome:<25} | "
                                f"{dias_atraso:<12} | "
                                f"{emprestimo.data_devolucao:<15}"
                            )
                            contador += 1
                    except ValueError:
                        pass 
        print("="*100)
        print(f"\nTotal de {contador} livros com devolução atrasada.")

    def contar_por_periodo(self, data_inicial_str, data_final_str):
        print("\n--- Relatório: Livros Emprestados por Período ---")
        
        try:
            data_inicial = datetime.strptime(data_inicial_str, '%d/%m/%Y')
            data_final = datetime.strptime(data_final_str, '%d/%m/%Y')
        except ValueError:
            print("ERRO: Formato de data inválido. Use DD/MM/AAAA.")
            return

        if data_inicial > data_final:
            print("ERRO: Data inicial deve ser anterior à data final.")
            return

        contador = 0
        
        for no in self.percorrer_inorder(self.indice.raiz):
            registro_str = self.ler_registro_no_arquivo(no.posicao_no_arquivo, self.ARQUIVO)
            
            if registro_str and not registro_str.startswith('*'):
                dados = registro_str.split(';')
                if len(dados) >= 4:
                    try:
                        data_emprestimo = datetime.strptime(dados[3], '%d/%m/%Y') 
                        
                        if data_inicial.date() <= data_emprestimo.date() <= data_final.date():
                            contador += 1
                    except ValueError:
                        pass
                        
        print(f"\nNo período de {data_inicial_str} a {data_final_str}, foram realizados **{contador}** empréstimos.")