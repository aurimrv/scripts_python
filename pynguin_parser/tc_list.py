#!/usr/bin/env python
'''
This utility list the number of a Pynguin generated tests set

USAGE:
     python tc_list.py <Pynguin test set>
'''
import ast
import sys
import random

# Classe responsável por alterar o node da AST desejado
class Transformer(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.testNumbers = []

    #Método visita apenas nós que definem FunctionDef. Aquelas que possuem decorator_list contendo 'strict'
    # são de interesse e serão alterados mudando o strict para False e removendo o último comando do body
    def visit_FunctionDef(self, node):
        name = node.name.split("_")
        if (len(name) == 3 and name[0] == "test" and name[1] == "case"):
            self.testNumbers.append(name[2])

        return node
    
    def getCounter(self):
        return len(self.testNumbers)
    
    def getTestNumbers(self):
        return self.testNumbers

def main(filename=None):
    if not filename:
        return

    with open(filename, 'r') as fp:
        data = fp.readlines()
    data = ''.join(data)
    tree = ast.parse(data)

    transformer = Transformer()
    transformer.visit(tree)

     # Corrige possíveis atributos faltantes nos nós
    ast.fix_missing_locations(tree)

    list=transformer.getTestNumbers()
    print(" ".join(list))  


if __name__ == '__main__':
    if len(sys.argv) <=1:
        print("\nUSAGE:\n\t tc_list.py <Pynguin test set>")
        sys.exit(1)
    else:
        main(sys.argv[1])