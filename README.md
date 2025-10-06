# 📚 Sistema de Gestão de Biblioteca

Este projeto simula um sistema de gestão para uma biblioteca, utilizando a lógica de **Arquivos Indexados** em Python. Os dados são armazenados de forma persistente em arquivos de texto no disco, enquanto a **Árvore Binária de Busca**.

O sistema foi estruturado com o padrão de design **Services** e **Modelos**.

---

## ⚙️ Arquitetura e Estrutura de Dados

O projeto implementa uma arquitetura de persistência baseada em índices:

* **Área de Índice:** Implementada como uma **Árvore Binária de Busca**. Cada nó armazena o **código** e o registro no arquivo.
* **Área de Dados:** Arquivos de texto (`.txt`) separados por entidade (e.g., `alunos.txt`, `livros.txt`).

### Estrutura de Módulos

* **`main.py`**: Ponto de entrada do sistema, responsável pela inicialização dos índices e gerenciamento dos menus.
* **`modelos/`**: Contém as classes que definem a estrutura de dados (e.g., `Aluno.py`, `Livro.py`).
* **`arvore/`**: Contém a classe `ArvoreBinaria.py` (o índice em memória).
* **`servicos/`**: Contém a lógica de negócio e persistência (e.g., `AlunoService.py`, `LivroService.py`).

---

## ✨ Funcionalidades Principais

O sistema implementa o ciclo completo de gestão de biblioteca:

### 1. Operações Básicas

As operações de **Inclusão**, **Consulta**, **Exclusão Lógica** (com marcação `*`) e **Leitura Exaustiva** são implementadas para **todas as tabelas** (`Alunos`, `Livros`, `Cidades`, etc.).

### 2. Lógica de Relacionamento

O sistema cruza dados de diferentes tabelas, garantindo que o usuário veja nomes e descrições em vez de apenas códigos:

* **Alunos:** Ao consultar um aluno, exibe a **Descrição do Curso** e a **Descrição/Estado da Cidade**.
* **Autores:** Ao consultar um autor, exibe o **Nome da Cidade** e o **Estado** de origem.
* **Livros:** Ao consultar um livro, exibe o **Nome do Autor** e a **Descrição da Categoria**.

### 3. Módulo de Empréstimos

O `EmprestimoService` lida com o controle de estoque e tempo:

* **Realizar Empréstimo:** Verifica se o livro está `disponivel`, define a **data de devolução (+7 dias)** e atualiza o status do livro para `emprestado`.
* **Realizar Devolução:** Verifica se o livro está **atrasado** e atualiza o status do empréstimo e do livro para `disponivel`.

### 4. Relatórios de Gestão

* **Listagem Ordenada:** A leitura exaustiva dos livros é realizada na ordem do código e mostra um resumo de status.
* **Relatórios de Atraso:** Lista livros atualmente **emprestados** e livros com **devolução atrasada**.

---

## ▶️ Como Instalar e Rodar o Projeto

O projeto é um aplicativo de console em Python, o que o torna muito fácil de iniciar. Basta garantir que você tenha o Python 3 instalado.

### 1. Instalação do Python

Siga as instruções para o seu sistema operacional se você ainda não tem o Python instalado:

| Sistema Operacional | Guia de Instalação |
| :--- | :--- |
| **Windows** | 1. Baixe o instalador do Python 3.x em [python.org/downloads/](https://www.python.org/downloads/). <br> 2. Durante a instalação, **marque a caixa** "Add Python to PATH" (Adicionar Python ao PATH). |
| **macOS/Linux** | O Python 3 geralmente já está instalado. Caso contrário, use `sudo apt install python3` (Linux) ou `brew install python` (macOS). |

### 2. Verificação e Execução

1.  **Verifique a Instalação:** Abra seu terminal e confirme que o Python está acessível:
    ```bash
    python3 --version
    ```

2.  **Navegue e Execute:** Use o comando `cd` para ir até o diretório raiz do projeto e inicie o sistema:
    ```bash
    # Exemplo de navegação:
    cd /caminho/para/TrabalhoBiblioteca/
    
    # Comando de Execução:
    python3 main.py
    # python main.py
    ```

O sistema será inicializado, reconstruindo todos os índices da **Árvore Binária de Busca**, e o **Menu Principal** será exibido, pronto para você gerenciar a biblioteca.
