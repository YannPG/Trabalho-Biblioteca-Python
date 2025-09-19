class Alunos:
    def __init__(self):
        self.codigo_aluno = None
        self.nome = None  
        self.codigo_curso = None
        self.codigo_cidade = None

    def cadastrarAluno(self, form :FormAluno):
        self.codigo_aluno = form.codigo_aluno
        self.nome = form.nome
        self.codigo_curso = form.codigo_cidade
        self.codigo_cidade = form.codigo_cidade