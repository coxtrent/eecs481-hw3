import ast
from pprint import pprint
import sys
import random
from copy import deepcopy

def tree_size(node):
    return 1 + sum(tree_size(child) for child in ast.iter_child_nodes(node))
class MutationChamber(ast.NodeTransformer):
    def __init__(self, dont_mutate_until):
        self.num_mutations = 0
        self.dont_mutate_until = dont_mutate_until
        self.nodes_so_far = 0
        self.max_mutations = 2
        # SECOND IDEA: we could just mutate the first node for the first mutant, 
        # the second node for the second mutant, etc.

        # THIRD IDEA: We could organize all the nodes in the tree by line number, 
        # and then mutate the nodes in order from the earliest line to the latest line.

        # LAST IDEA AND THE FIRST ONE WE'LL TRY: 
        # Randomly decide whether to mutate each node as we look at it using random.choice([True, False])random.choice([True, False]) and num_mutations < 2, setting random.seed(num_mutants) at the start of the program.

    def visit_Compare(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until and self.num_mutations < self.max_mutations):
            self.num_mutations += 1
            if isinstance(node.ops[0], ast.GtE):
                node.ops[0] = ast.Lt()
            elif isinstance(node.ops[0], ast.Gt):
                node.ops[0] = ast.LtE()
            elif isinstance(node.ops[0], ast.LtE):
                node.ops[0] = ast.Gt()
            elif isinstance(node.ops[0], ast.Lt):
                node.ops[0] = ast.GtE()
            elif isinstance(node.ops[0], ast.Eq):
                node.ops[0] = ast.NotEq()
            elif isinstance(node.ops[0], ast.NotEq):
                node.ops[0] = ast.Eq()
        self.nodes_so_far += 1
        return node

    def visit_If(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until  and self.num_mutations < self.max_mutations):
            self.num_mutations += 1
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.ops[0], ast.GtE):
                    node.ops[0] = ast.Lt()
                elif isinstance(node.test.ops[0], ast.Gt):
                    node.ops[0] = ast.LtE()
                elif isinstance(node.test.ops[0], ast.LtE):
                    node.ops[0] = ast.Gt()
                elif isinstance(node.test.ops[0], ast.Lt):
                    node.ops[0] = ast.GtE()
                elif isinstance(node.test.ops[0], ast.Eq):
                    node.ops[0] = ast.NotEq()
                elif isinstance(node.test.ops[0], ast.NotEq):
                    node.ops[0] = ast.Eq()
            self.nodes_so_far += 1
            return node

    def visit_BinOp(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until and self.num_mutations < self.max_mutations):
            self.num_mutations += 1
            if isinstance(node.op, ast.Add):
                node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                node.op = ast.Add()
            elif isinstance(node.op, ast.Mult):
                node.op = ast.FloorDiv()
            elif isinstance(node.op, ast.FloorDiv):
                node.op = ast.Mult()
        self.nodes_so_far += 1
        return node

    def visit_Subscript(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until and self.num_mutations < self.max_mutations):
            self.num_mutations += 1
            if isinstance(node.slice, ast.Index):
                if isinstance(node.slice.value, ast.Constant) and isinstance(node.slice.value.value, int):
            # Add or subtract 1 from the subscript
                    if random.choice([True, False]):
                        node.slice.value.n += 1
                    else:
                        node.slice.value.n -= 1
        self.nodes_so_far += 1
        return node
    
    def visit_Assign(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until and self.num_mutations < self.max_mutations):
            self.nodes_so_far += 1
            self.num_mutations += 1
            return ast.Pass() 
        else:
            self.nodes_so_far += 1
            self.num_mutations += 1
            return node
        
    def visit_Call(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until and self.num_mutations < self.max_mutations):
            self.nodes_so_far += 1
            return ast.Pass()
        else:
            self.nodes_so_far += 1
            self.num_mutations += 1
            return node


def main(args):
    "Parse command line, return errors if necessary, and call mutationChamber."
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
        random.seed(num_mutants)
        
    treesize = tree_size(tree)
    print("Tree size: ", treesize)
    mutationChamber(tree, num_mutants)

def mutationChamber(tree, num_mutants):
    """I will mootate you. I will mootate you all."""
    for i in range(num_mutants):
        mutator = MutationChamber(i)
        mutant_tree = mutator.visit(deepcopy(tree))
        mutant_src = ast.unparse(mutant_tree)
        with open(str(i) + ".py", "w") as mutant:
            mutant.write(mutant_src)
    return


def printUsage():
    print("USAGE: mutate.py <filename> <number of mutants>")

        
if __name__ == "__main__":
    main(sys.argv)


