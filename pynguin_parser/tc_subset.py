#!/usr/bin/env python
'''
This utility creates a subset of test cases based on a Pynguin test set

USAGE:
     python tc_subset.py <Pynguin test set> <test case numbers to be considered>
'''
import ast
import sys

# Classe responsável por alterar o node da AST desejado
class Transformer(ast.NodeTransformer):
    def __init__(self,testCaseNumbers) -> None:
        super().__init__()
        self.testCaseNumbers=testCaseNumbers

    #Método visita apenas nós que definem FunctionDef. Aquelas que possuem decorator_list contendo 'strict'
    # são de interesse e serão alterados mudando o strict para False e removendo o último comando do body
    def visit_FunctionDef(self, node):
        name = node.name.split("_")
        if (len(name) == 3 and name[0] == "test" and name[1] == "case"):
            if (name[2] not in self.testCaseNumbers):
               node = None

        return node
    
def main(args=None):
   if not args:
      return
   
   filename = args[1]

   with open(filename, 'r') as fp:
      data = fp.readlines()
   data = ''.join(data)
   tree = ast.parse(data)

   print("#Pyguin test cases subset from %s" % filename)

   testCaseNumbers = args[2:]
      
   transformer = Transformer(testCaseNumbers)
   transformer.visit(tree)

   # Corrige possíveis atributos faltantes nos nós
   ast.fix_missing_locations(tree)

   print(ast.unparse(tree))

if __name__ == '__main__':
    if len(sys.argv) <=2:
        print("\nUSAGE:\n\t tc_subset.py <Pynguin test set> <test case numbers to be considered>")
        print("\t\nExample:\n\t tc_subset.py ./test_binarySearchTree1_MIO.py 0 10 12 15")
        sys.exit(1)
    else:
        main(sys.argv)