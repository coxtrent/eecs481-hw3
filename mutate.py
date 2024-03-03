import ast
from pprint import pprint
import sys


def main(args):
    # parse command line, return errors
    num_mutants, filename, tree = None, None, None
    if len(args) == 3:
        try:
            filename = args[1]
            num_mutants = int(args[2])
        except ValueError:
            print('Second argument is not an integer')
            printUsage()
    else:
        printUsage()

    with open(filename, "r") as src:
        tree = ast.parse(src.read())

    mutationChamber(tree, num_mutants)

def mutationChamber(tree, num_mutants):
    print(ast.dump(tree))
    print(num_mutants)
    return


def printUsage():
    print("USAGE: mutate.py <filename> <number of mutants>")

        
if __name__ == "__main__":
    main(sys.argv)
