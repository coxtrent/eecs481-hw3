import ast
from pprint import pprint
import sys
import random
from copy import deepcopy
import astor

def tree_size(node):
    return 1 + sum(tree_size(child) for child in ast.iter_child_nodes(node))

class FunctionCounter(ast.NodeVisitor):
    def __init__(self):
        self.function_call_count = {}
        self.function_tree_size = {}
        self.function_defs = set()
        self.num_defs = 0
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.function_call_count:
                self.function_call_count[node.func.id] += 1
            else:
                self.function_call_count[node.func.id] = 1
                self.function_tree_size[node.func.id] = tree_size(node)
        # special key that is number of definitions, 
        # has a space so it never gets overwritten by a function name
        
        return node
    
    def visit_FunctionDef(self, node):
        #print(f"Visiting function: {node.name}")
        self.function_defs.add(node.name)
        self
        self.num_defs += 1
        self.generic_visit(node)


    def getTreeData(self):
        self.function_call_count = {key: val for key, val  in self.function_call_count.items() if key in self.function_defs}
        
        return {"call_count": self.function_call_count, "func_tree_size": self.function_tree_size}


class NodeFinder(ast.NodeTransformer):
    def __init__(self, func_name, dont_mutate_until, max_mutations, mutants_so_far):
        self.dont_mutate_until = dont_mutate_until
        self.func_to_mutate = func_name
        self.max_mutations = max_mutations
        self.mutants_so_far = mutants_so_far

    def visit_FunctionDef(self, node):
        if node.name == self.func_to_mutate:
            mutator = MutationChamber(mutants_so_far=self.mutants_so_far, dont_mutate_until=self.dont_mutate_until, max_mutations=self.max_mutations)
            node = mutator.visit(node)
        print(node)
        #breakpoint()
        return node

class MutationChamber(ast.NodeTransformer):
    def __init__(self, mutants_so_far, dont_mutate_until: int, max_mutations: int = 1, ):
        self.num_mutations = 0
        self.dont_mutate_until = dont_mutate_until
        self.nodes_so_far = 0
        self.max_mutations = max_mutations
        self.mutants_so_far = mutants_so_far
        # SECOND IDEA: we could just mutate the first node for the first mutant, 
        # the second node for the second mutant, etc.

        # THIRD IDEA: We could organize all the nodes in the tree by line number, 
        # and then mutate the nodes in order from the earliest line to the latest line.


        # LAST IDEA AND THE FIRST ONE WE'LL TRY: 
        # Randomly decide whether to mutate each node as we look at it using random.choice([True, False])random.choice([True, False]) and num_mutations < 2, setting random.seed(num_mutants) at the start of the program.

    def shouldMutate(self, node):
        return self.nodes_so_far >= self.dont_mutate_until and self.num_mutations < self.max_mutations

    def visit_Compare(self, node):
        if(self.shouldMutate(node)):
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
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node


    def visit_If(self, node):
        if(self.nodes_so_far >= self.dont_mutate_until  and self.num_mutations < self.max_mutations):
            self.num_mutations += 1
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.ops[0], ast.GtE):
                    node.test.ops[0] = ast.Lt()
                elif isinstance(node.test.ops[0], ast.Gt):
                    node.test.ops[0] = ast.LtE()
                elif isinstance(node.test.ops[0], ast.LtE):
                    node.test.ops[0] = ast.Gt()
                elif isinstance(node.test.ops[0], ast.Lt):
                    node.test.ops[0] = ast.GtE()
                elif isinstance(node.test.ops[0], ast.Eq):
                    node.test.ops[0] = ast.NotEq()
                elif isinstance(node.test.ops[0], ast.NotEq):
                    node.test.ops[0] = ast.Eq()
        self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node
    

    def visit_Constant(self, node):
        if(self.shouldMutate(node)):
            self.num_mutations += 1
            if node.value is True:
                node.value = False
            elif node.value is False:
                node.value = True
        self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node


    def visit_BinOp(self, node):
        if(self.shouldMutate(node)):
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
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node


    def visit_BoolOp(self, node):
        if(self.shouldMutate(node)):
            self.num_mutations += 1
            if isinstance(node.op, ast.And):
                node.op = ast.Or()
            elif isinstance(node.op, ast.Or):
                node.op = ast.And()
        self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node


    """  def visit_Subscript(self, node):
        if(self.shouldMutate(node)):
            self.num_mutations += 1
            if isinstance(node.slice, ast.Index):
                if isinstance(node.slice.value, ast.Constant) and isinstance(node.slice.value.value, int):
            # Add or subtract 1 from the subscript
                    if random.choice([True, False]):
                        node.slice.value.n += 1
                    else:
                        node.slice.value.n -= 1
        self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node"""


    def visit_Assign(self, node):
        if(self.shouldMutate(node)):
            self.nodes_so_far += 1
            self.num_mutations += 1
            return ast.Pass() 
        else:
            self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node


    def visit_Call(self, node):
        if(self.shouldMutate(node)):
            self.nodes_so_far += 1
            self.num_mutations
            return ast.Pass()
        else:
            self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node

        
"""    def visit_FunctionDef(self, node):
        print(node.name)
        self.nodes_so_far += 1
#        print(f"Visiting node: {ast.dump(node)}")
#        print("\n")
#        print(f"Returning: {node}")
#        print("\n")
        return node"""


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
    ctr = FunctionCounter()
    ctr.visit(tree)
    treeData = ctr.getTreeData()
    treeData["call_count"] = sorted(treeData["call_count"].items(), key=lambda x: x[1], reverse=True)
    pprint(treeData)
    #breakpoint()
    mutants_so_far = 0
    current_max_mutations = 1
    old_mutants = []
    #breakpoint()
    while(mutants_so_far < num_mutants):
        for(func_name, call_count) in treeData["call_count"]:
            if(mutants_so_far >= num_mutants):
                        break
            """First, we're going to try mutating each node of the most called, then each of the next...
            If that doesn't work, then we're going to try mutating the first of the first, then 1st of the 2nd, etc. 
            until we loop through all functions and go back to mutating the second node of the first.
            We will use autograder to compare results from each strategy."""
            # TODO: RIGHT NOW WE ARE MUTATING ALL LINES OF EACH FUNCTION BEFORE GOING TO THE NEXT FUNCTION
            if(call_count > 2):
                for i in range(treeData["func_tree_size"][func_name]):
                    mutator = NodeFinder(func_name, random.randint(1, treeData["func_tree_size"][func_name]), current_max_mutations, mutants_so_far)
                    mutant_tree = deepcopy(tree)
                    #breakpoint()
                    mutant_tree = mutator.visit(mutant_tree)
                    mutant_src = astor.to_source(mutant_tree) # ast.unparse(mutant_tree) 
                    if(mutant_tree != tree and mutant_tree not in old_mutants):
                        with open(str(mutants_so_far) + ".py", "w") as mutant:
                            mutant.write(mutant_src)
                            old_mutants.append(mutant_tree)
                        mutants_so_far += 1
                    if(mutants_so_far >= num_mutants):
                        break
                #breakpoint()
        current_max_mutations += 1
    #breakpoint()
        #mutator = MutationChamber(i)
        #mutant_tree = mutator.visit(deepcopy(tree))
        #mutant_src = ast.unparse(mutant_tree)
       
    return


def printUsage():
    print("USAGE: mutate.py <filename> <number of mutants>")

        
if __name__ == "__main__":
    main(sys.argv)


