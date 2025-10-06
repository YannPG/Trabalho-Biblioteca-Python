class Emprestimo:
    def __init__(self, codigo_emprestimo, codigo_livro, codigo_aluno, data_emprestimo, data_devolucao, devolvido):
        self.codigo_emprestimo = codigo_emprestimo
        self.codigo_livro = codigo_livro
        self.codigo_aluno = codigo_aluno
        self.data_emprestimo = data_emprestimo       
        self.data_devolucao = data_devolucao         
        self.devolvido = devolvido                   