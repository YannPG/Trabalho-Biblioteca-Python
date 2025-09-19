class NoArvore:
    def __init__(self, codigo, posicaoNoArquivo):
        self.codigo = codigo 
        self.posicaoNoArquivo = posicaoNoArquivo 
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigoAluno, posicaoNoArquivo):
            novoNo = NoArvore(codigoAluno, posicaoNoArquivo)
            if self.raiz is None:
                self.raiz = novoNo
            else:
                self.inserirRecursivo(self.raiz, novoNo)

    def inserirRecursivo(self, noAtual, novoNo):
        if novoNo.codigo < noAtual.codigo:
            if noAtual.esquerda is None:
                noAtual.esquerda = novoNo
            else:
                self.inserirRecursivo(noAtual.esquerda, novoNo)
        elif novoNo.codigo > noAtual.codigo:
            if noAtual.direita is None:
                noAtual.direita = novoNo
            else:
                self.inserirRecursivo(noAtual.direita, novoNo)
        else:
            print("Erro: Código de aluno já existe!")
            
    def buscar(self, codigoAluno):
        return self.buscarRecursivo(self.raiz, codigoAluno)

    def buscarRecursivo(self, noAtual, codigoAluno):
        if noAtual is None or noAtual.codigo == codigoAluno:
            return noAtual
        if codigoAluno < noAtual.codigo:
            return self.buscarRecursivo(noAtual.esquerda, codigoAluno)
        return self.buscarRecursivo(noAtual.direita, codigoAluno)
    