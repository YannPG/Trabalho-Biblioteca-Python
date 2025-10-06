import os
from datetime import datetime, timedelta


from arvore.ArvoreBinaria import ArvoreBinaria, NoArvore 
from modelos.Aluno import Aluno
from modelos.Autor import Autor 
from modelos.Cidade import Cidade
from modelos.Curso import Curso
from modelos.Categoria import Categoria 
from modelos.Livro import Livro
from modelos.Emprestimo import Emprestimo 

from servicos.AlunoService import AlunoService 
from servicos.CidadeService import CidadeService 
from servicos.CursoService import CursoService   
from servicos.AutorService import AutorService 
from servicos.CategoriaService import CategoriaService 
from servicos.LivroService import LivroService 
from servicos.EmprestimoService import EmprestimoService 

indice_alunos = ArvoreBinaria(); ARQUIVO_ALUNOS = "alunos.txt"
indice_cidades = ArvoreBinaria(); ARQUIVO_CIDADES = "cidades.txt"
indice_cursos = ArvoreBinaria(); ARQUIVO_CURSOS = "cursos.txt"
indice_autores = ArvoreBinaria(); ARQUIVO_AUTORES = "autores.txt"
indice_categorias = ArvoreBinaria(); ARQUIVO_CATEGORIAS = "categorias.txt"
indice_livros = ArvoreBinaria(); ARQUIVO_LIVROS = "livros.txt"
indice_emprestimos = ArvoreBinaria(); ARQUIVO_EMPRESTIMOS = "emprestimos.txt"

aluno_service = None
cidade_service = None
curso_service = None
autor_service = None
categoria_service = None
livro_service = None 
emprestimo_service = None 


def percorrer_inorder(no):
    if no:
        yield from percorrer_inorder(no.esquerda)
        yield no
        yield from percorrer_inorder(no.direita)

def ler_registro_no_arquivo(posicao, arquivo):
    try:
        with open(arquivo, 'r') as dados_do_arquivo:
            dados_do_arquivo.seek(posicao)
            registro_str = dados_do_arquivo.readline().strip() 
            return registro_str
    except FileNotFoundError:
        return None

def marcar_registro_como_excluido(posicao, arquivo_nome):
    try:
        with open(arquivo_nome, 'r+') as dados_do_arquivo: 
            dados_do_arquivo.seek(posicao)
            primeiro_caractere = dados_do_arquivo.read(1)
            dados_do_arquivo.seek(posicao)
            
            if primeiro_caractere != '*':
                dados_do_arquivo.write('*') 
    except Exception as e:
        print(f"ERRO ao marcar registro: {e}")


def buscar_cidade_por_codigo(codigo_cidade):
    try:
        codigo_int = int(codigo_cidade)
    except (ValueError, TypeError):
        return None
    no_encontrado = indice_cidades.buscar(codigo_int)
    if no_encontrado:
        registro_str = ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, ARQUIVO_CIDADES)
        if registro_str and not registro_str.startswith('*'):
            dados = registro_str.split(';')
            if len(dados) >= 3: return Cidade(int(dados[0]), dados[1], dados[2])
    return None

def buscar_curso_por_codigo(codigo_curso):
    try:
        codigo_int = int(codigo_curso)
    except (ValueError, TypeError):
        return None
    no_encontrado = indice_cursos.buscar(codigo_int)
    if no_encontrado:
        registro_str = ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, ARQUIVO_CURSOS)
        if registro_str and not registro_str.startswith('*'):
            dados = registro_str.split(';')
            if len(dados) >= 2: return Curso(int(dados[0]), dados[1])
    return None

def buscar_autor_por_codigo(codigo_autor):
    try: codigo_int = int(codigo_autor)
    except (ValueError, TypeError): return None
    no_encontrado = indice_autores.buscar(codigo_int)
    if no_encontrado:
        registro_str = ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, ARQUIVO_AUTORES)
        if registro_str and not registro_str.startswith('*'):
            dados = registro_str.split(';')
            if len(dados) >= 3: return Autor(int(dados[0]), dados[1], dados[2])
    return None

def buscar_categoria_por_codigo(codigo_categoria):
    try: codigo_int = int(codigo_categoria)
    except (ValueError, TypeError): return None
    no_encontrado = indice_categorias.buscar(codigo_int)
    if no_encontrado:
        registro_str = ler_registro_no_arquivo(no_encontrado.posicao_no_arquivo, ARQUIVO_CATEGORIAS)
        if registro_str and not registro_str.startswith('*'):
            dados = registro_str.split(';')
            if len(dados) >= 2: return Categoria(int(dados[0]), dados[1])
    return None


def _salvar_e_indexar(objeto, indice, arquivo_nome, campos):
    try:
        with open(arquivo_nome, 'a') as dados_do_arquivo:
            posicao = dados_do_arquivo.tell() 
            registro_str = ";".join(str(getattr(objeto, campo)) for campo in campos) + "\n"
            dados_do_arquivo.write(registro_str)
            
            codigo = getattr(objeto, campos[0])
            if indice.buscar(codigo):
                 print(f"AVISO: Código {codigo} já existia no índice. Não inserido.")
            else:
                indice.inserir(codigo, posicao)
        print(f"SUCESSO: Registro com código {codigo} incluído em {arquivo_nome}.")
        return True
    except Exception as e:
        print(f"ERRO ao incluir em {arquivo_nome}: {e}")
        return False

def incluir_cidade():
    while True:
        try:
            codigo = int(input("Código da Cidade: "))
            if indice_cidades.buscar(codigo):
                print("Código já existe.")
                continue
            descricao = input("Descrição da Cidade: ")
            estado = input("Estado (Ex: SP): ")
            nova_cidade = Cidade(codigo, descricao, estado)
            campos = ['codigo_cidade', 'descricao', 'estado']
            if _salvar_e_indexar(nova_cidade, indice_cidades, ARQUIVO_CIDADES, campos):
                break
        except ValueError:
            print("Código inválido. Tente novamente.")

def incluir_curso():
    while True:
        try:
            codigo = int(input("Código do Curso: "))
            if indice_cursos.buscar(codigo):
                print("Código já existe.")
                continue
            descricao = input("Descrição do Curso: ")
            novo_curso = Curso(codigo, descricao)
            campos = ['codigo_curso', 'descricao']
            if _salvar_e_indexar(novo_curso, indice_cursos, ARQUIVO_CURSOS, campos):
                break
        except ValueError:
            print("Código inválido. Tente novamente.")

def incluir_autor():
    while True:
        try:
            codigo = int(input("Código do Autor: "))
            if indice_autores.buscar(codigo):
                print("Código já existe.")
                continue
            nome = input("Nome do Autor: ")
            codigo_cidade = input("Código da Cidade Natal: ")
            
            novo_autor = Autor(codigo, nome, codigo_cidade)
            campos = ['codigo_autor', 'nome', 'codigo_cidade']
            
            if _salvar_e_indexar(novo_autor, indice_autores, ARQUIVO_AUTORES, campos):
                break
        except ValueError:
            print("Entrada inválida. Tente novamente.")
        except NameError:
             print("ERRO: A classe 'Autor' pode não estar importada ou definida corretamente. Verifique 'modelos/Autor.py'.")

def _reconstruir_indice(indice_arvore, nome_arquivo):
    indice_arvore.raiz = None
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'w') as dados_do_arquivo: pass
    
    posicao_atual = 0
    with open(nome_arquivo, 'r') as dados_do_arquivo:
        for linha in dados_do_arquivo:
            if linha.strip() and not linha.startswith('*'):
                try:
                    codigo = int(linha.split(';')[0]) 
                    indice_arvore.inserir(codigo, posicao_atual)
                except Exception: pass
            posicao_atual += len(linha)


def inicializar_sistema():
    global indice_alunos, indice_cidades, indice_cursos, indice_autores, indice_categorias, indice_livros, indice_emprestimos
    global aluno_service, cidade_service, curso_service, autor_service, categoria_service, livro_service, emprestimo_service
    
    _reconstruir_indice(indice_alunos, ARQUIVO_ALUNOS)
    _reconstruir_indice(indice_cidades, ARQUIVO_CIDADES)
    _reconstruir_indice(indice_cursos, ARQUIVO_CURSOS)
    _reconstruir_indice(indice_autores, ARQUIVO_AUTORES) 
    _reconstruir_indice(indice_categorias, ARQUIVO_CATEGORIAS) 
    _reconstruir_indice(indice_livros, ARQUIVO_LIVROS)
    _reconstruir_indice(indice_emprestimos, ARQUIVO_EMPRESTIMOS)
    
    aluno_service = AlunoService(
        ARQUIVO_ALUNOS, indice_alunos, ler_registro_no_arquivo,
        percorrer_inorder, buscar_curso_por_codigo, buscar_cidade_por_codigo, 
        marcar_registro_como_excluido)


    cidade_service = CidadeService(
        ARQUIVO_CIDADES, indice_cidades, ler_registro_no_arquivo,
        percorrer_inorder, marcar_registro_como_excluido
    )

    curso_service = CursoService(
        ARQUIVO_CURSOS, indice_cursos, ler_registro_no_arquivo,
        percorrer_inorder, marcar_registro_como_excluido
    )

    autor_service = AutorService(
        ARQUIVO_AUTORES, indice_autores, ler_registro_no_arquivo,
        percorrer_inorder, marcar_registro_como_excluido,
        buscar_cidade_por_codigo
    )

    categoria_service = CategoriaService( 
        ARQUIVO_CATEGORIAS, indice_categorias, ler_registro_no_arquivo,
        percorrer_inorder, marcar_registro_como_excluido
    )

    livro_service = LivroService( 
        ARQUIVO_LIVROS, indice_livros, ler_registro_no_arquivo,
        percorrer_inorder, marcar_registro_como_excluido,
        buscar_autor_por_codigo,        
        buscar_categoria_por_codigo,    
        buscar_cidade_por_codigo        
    )

    emprestimo_service = EmprestimoService(
        ARQUIVO_EMPRESTIMOS, indice_emprestimos, ler_registro_no_arquivo,
        percorrer_inorder, marcar_registro_como_excluido,
        livro_service, 
        aluno_service  
    )


def menu_alunos():
    while True:
        print("\n--- Módulo Alunos (Operações Básicas) ---")
        print("1 - Incluir Novo Aluno")
        print("2 - Consultar Aluno")
        print("3 - Excluir Aluno")
        print("4 - Listar Todos")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            aluno_service.incluir_aluno()
        elif opcao == '2':
            try:
                codigo_consulta = int(input("Digite o Código do Aluno para consulta: "))
                aluno_service.consultar_aluno(codigo_consulta)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '3':
            try:
                codigo_excluir = int(input("Digite o Código do Aluno para exclusão: "))
                aluno_service.excluir_aluno(codigo_excluir)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '4':
            aluno_service.leitura_exaustiva()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_cidades():
    while True:
        print("\n--- Módulo Cidades ---")
        print("1 - Incluir Cidade")
        print("2 - Consultar Cidade")
        print("3 - Excluir Cidade")
        print("4 - Listar Todas")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            codigo = int(input("Código da Cidade: "))
            descricao = input("Descrição da Cidade: ")
            estado = input("Estado (Ex: SP): ")
            cidade_service.incluir_registro(codigo, descricao, estado)
        elif opcao == '2':
            codigo = int(input("Código da Cidade para consulta: "))
            cidade_service.consultar_registro(codigo)
        elif opcao == '3':
            codigo = int(input("Código da Cidade para exclusão: "))
            cidade_service.excluir_registro(codigo)
        elif opcao == '4':
            cidade_service.leitura_exaustiva()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_cursos():
    while True:
        print("\n--- Módulo Cursos ---")
        print("1 - Incluir Curso")
        print("2 - Consultar Curso")
        print("3 - Excluir Curso")
        print("4 - Listar Todos")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            codigo = int(input("Código do Curso: "))
            descricao = input("Descrição do Curso: ")
            curso_service.incluir_registro(codigo, descricao)
        elif opcao == '2':
            codigo = int(input("Código do Curso para consulta: "))
            curso_service.consultar_registro(codigo)
        elif opcao == '3':
            codigo = int(input("Código do Curso para exclusão: "))
            curso_service.excluir_registro(codigo)
        elif opcao == '4':
            curso_service.leitura_exaustiva()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_autores():
    while True:
        print("\n--- Módulo Autores ---")
        print("1 - Incluir Autor")
        print("2 - Consultar Autor")
        print("3 - Excluir Autor")
        print("4 - Listar Todos")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            incluir_autor()
        elif opcao == '2':
            try:
                codigo = int(input("Código do Autor para consulta: "))
                autor_service.consultar_registro(codigo)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '3':
            try:
                codigo = int(input("Código do Autor para exclusão: "))
                autor_service.excluir_registro(codigo)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '4':
            autor_service.leitura_exaustiva()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_categorias():
    while True:
        print("\n--- Módulo Categorias ---")
        print("1 - Incluir Categoria")
        print("2 - Consultar Categoria")
        print("3 - Excluir Categoria")
        print("4 - Listar Todas")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            try:
                codigo = int(input("Código da Categoria: "))
                descricao = input("Descrição da Categoria: ")
                categoria_service.incluir_registro(codigo, descricao)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '2':
            try:
                codigo = int(input("Código da Categoria para consulta: "))
                categoria_service.consultar_registro(codigo)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '3':
            try:
                codigo = int(input("Código da Categoria para exclusão: "))
                categoria_service.excluir_registro(codigo)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '4':
            categoria_service.leitura_exaustiva()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_livros():
    while True:
        print("\n--- Módulo Livros ---")
        print("1 - Incluir Novo Livro")
        print("2 - Consultar Livro")
        print("3 - Excluir Livro")
        print("4 - Listar Todos")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            livro_service.incluir_registro() 
        elif opcao == '2':
            try:
                codigo = int(input("Código do Livro para consulta: "))
                livro_service.consultar_registro(codigo)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '3':
            try:
                codigo = int(input("Código do Livro para exclusão: "))
                livro_service.excluir_registro(codigo)
            except ValueError:
                print("Entrada inválida. O código deve ser um número inteiro.")
        elif opcao == '4':
            livro_service.leitura_exaustiva() 
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_emprestimos():
    while True:
        print("\n--- Módulo Empréstimos ---")
        print("1 - Realizar Novo Empréstimo")
        print("2 - Realizar Devolução")
        print("3 - Consultas e Relatórios")
        print("0 - Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            emprestimo_service.realizar_emprestimo()
        elif opcao == '2':
            emprestimo_service.realizar_devolucao()
        elif opcao == '3':
            menu_relatorios_emprestimos()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_relatorios_emprestimos():
    while True:
        print("\n--- Submenu de Relatórios ---")
        print("1 - Livros Emprestados")
        print("2 - Livros com Devolução Atrasada")
        print("3 - Livros Emprestados por Período")
        print("0 - Voltar ao Menu Empréstimos")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            emprestimo_service.listar_emprestados()
        elif opcao == '2':
            emprestimo_service.listar_atrasados()
        elif opcao == '3':
            data_inicial = input("Data Inicial (DD/MM/AAAA): ")
            data_final = input("Data Final (DD/MM/AAAA): ")
            emprestimo_service.contar_por_periodo(data_inicial, data_final)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    inicializar_sistema()
    
    while True:
        print("\n*** MENU PRINCIPAL ***")
        print("1 - Gerenciar Alunos")
        print("2 - Gerenciar Cidades")
        print("3 - Gerenciar Cursos")
        print("4 - Gerenciar Autores")
        print("5 - Gerenciar Categorias")
        print("6 - Gerenciar Livros")
        print("7 - Gerenciar Empréstimos")
        print("0 - Sair do Sistema")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            menu_alunos()
        elif opcao == '2':
            menu_cidades()
        elif opcao == '3':
            menu_cursos()
        elif opcao == '4':
            menu_autores()
        elif opcao == '5':
            menu_categorias()
        elif opcao == '6':
            menu_livros() 
        elif opcao == '7':
            menu_emprestimos()
        elif opcao == '0':
            print("Sistema encerrado!")
            break
        else:
            print("Opção inválida. Tente novamente.")