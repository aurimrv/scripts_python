#!/usr/bin/env python
'''
This utility converts the Pynguin test case with Strict command on runnable test cases.

USAGE:
     python transformer.py <Pynguin original test filename>
'''
import ast
import sys

# Classe responsável por alterar o node da AST desejado
class Transformer(ast.NodeTransformer):
    #Método visita apenas nós que definem FunctionDef. Aquelas que possuem decorator_list contendo 'strict'
    # são de interesse e serão alterados mudando o strict para False e removendo o último comando do body
    def visit_FunctionDef(self, node):
        if (len(node.decorator_list)>0):
            for i in range(0,len(node.decorator_list)):
                e = node.decorator_list[i]
                if (isinstance(e,ast.Call)):
                    # Assumindo que sempre o strict será o primeiro elemento da lista.
                    k = e.keywords[0]
                    # Function with 'strict' annotation, change to False and remove last body statement
                    if (k.arg == 'strict'):
                        k.value=ast.Constant(value=False)
                        node.body = node.body[:-1]
                        #Removendo decorator strict
                        del(node.decorator_list[i])
        return node

def main(filename=None):
    if not filename:
        return

    with open(filename, 'r') as fp:
        data = fp.readlines()
    data = ''.join(data)
    tree = ast.parse(data)

    print("#Pyguin test cases converted from %s" % filename)

    Transformer().visit(tree)
    
    # Corrige possíveis atributos faltantes nos nós
    ast.fix_missing_locations(tree)

    print(ast.unparse(tree))

if __name__ == '__main__':
    if len(sys.argv) <=1:
        print("\nUSAGE:\n\t transformer.py <Pynguin original test filename>")
        sys.exit(1)
    else:
        main(sys.argv[1])