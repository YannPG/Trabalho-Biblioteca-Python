class NoArvore:
    def __init__(self, codigo, posicao_no_arquivo):
        self.codigo = codigo 
        self.posicao_no_arquivo = posicao_no_arquivo 
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None
        self.posicao_removida = None

    def inserir(self, codigo, posicao_no_arquivo):
        novoNo = NoArvore(codigo, posicao_no_arquivo)
        if self.raiz is None:
            self.raiz = novoNo
        else:
            self.raiz = self._inserir_recursivo(self.raiz, novoNo)
    
    def _inserir_recursivo(self, no_atual, novo_no):
        if novo_no.codigo < no_atual.codigo:
            if no_atual.esquerda is None:
                no_atual.esquerda = novo_no
            else:
                self._inserir_recursivo(no_atual.esquerda, novo_no)
        elif novo_no.codigo > no_atual.codigo:
            if no_atual.direita is None:
                no_atual.direita = novo_no
            else:
                self._inserir_recursivo(no_atual.direita, novo_no)
        else:
            pass
        return no_atual

    def buscar(self, codigo):
        return self._buscar_recursivo(self.raiz, codigo)

    def _buscar_recursivo(self, noAtual, codigo):
        if noAtual is None or noAtual.codigo == codigo:
            return noAtual
        if codigo < noAtual.codigo:
            return self._buscar_recursivo(noAtual.esquerda, codigo)
        return self._buscar_recursivo(noAtual.direita, codigo)
    
    def remover(self, codigo):
        self.posicao_removida = None 
        self.raiz = self._remover_recursivo(self.raiz, codigo)
        return self.posicao_removida

    def _encontrar_sucessor_e_remover_minimo(self, no_atual):
        if no_atual.esquerda is None:
            return no_atual
        
        no_atual.esquerda = self._encontrar_sucessor_e_remover_minimo(no_atual.esquerda)
        return no_atual

    def _remover_recursivo(self, no_atual, codigo):
        if no_atual is None:
            return no_atual

        if codigo < no_atual.codigo:
            no_atual.esquerda = self._remover_recursivo(no_atual.esquerda, codigo)
        elif codigo > no_atual.codigo:
            no_atual.direita = self._remover_recursivo(no_atual.direita, codigo)
        else:
            self.posicao_removida = no_atual.posicao_no_arquivo
            
            if no_atual.esquerda is None:
                return no_atual.direita
            elif no_atual.direita is None:
                return no_atual.esquerda

            sucessor = self._encontrar_minimo(no_atual.direita)
            
            no_atual.codigo = sucessor.codigo
            no_atual.posicao_no_arquivo = sucessor.posicao_no_arquivo

            no_atual.direita = self._remover_recursivo(no_atual.direita, sucessor.codigo)
            
        return no_atual

    def _encontrar_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual