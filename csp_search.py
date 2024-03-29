from utils import *
from csp import *

# CSP Search


# Variable ordering

def first_unassigned_variable(assignment, csp):
    "The default variable order."
    return find_if(lambda var: var not in assignment, csp.vars)
    
def mrv(assignment, csp):
    "Minimum-remaining-values heuristic."
 
    def num_legal_values(csp, var):
        return len(csp.domains[var]) 
           
    "tie goes to the first one"
    return argmin(
        [v for v in csp.vars if v not in assignment],
        lambda var: num_legal_values(csp, var))

""" "breaks ties at random"
    return argmin_random_tie(
        [v for v in csp.vars if v not in assignment],
        lambda var: num_legal_values(csp, var))"""


# Inference

def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    "Prune neighbor values inconsistent with var=value."
    for B in csp.neighbors[var]:            
        if B not in assignment:                 
            for b in csp.domains[B][:]:
                forward_checking.has_conflict_counter += 1
                csp.assign(B, b, assignment)
                if csp.has_conflict(var, value, assignment) == True:
                    csp.prune(B, b, removals)
                csp.unassign(B, assignment)
            if not csp.domains[B]:
                return False
    return True
forward_checking.has_conflict_counter = 0

def mac(csp, var, value, assignment, removals):
    "Maintain arc consistency."
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)


def AC3(csp, queue=None, removals=None):
    "Constraint Propagation"
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]    
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    
    return True

def revise(csp, Xi, Xj, removals):
    "Return true if we remove a value."
    revised = False
    for x in csp.domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every( lambda y: csp.arc_conflict(Xi, x, Xj, y), csp.domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised
# The backtracking search

def backtracking_search(csp,
                        select_unassigned_variable = first_unassigned_variable,                        
                        inference = no_inference):   
    
    def backtrack(assignment):
        if len(assignment) == len(csp.vars):
            return assignment 
        var = select_unassigned_variable(assignment, csp)        
        for value in csp.domains[var]:
            if csp.has_conflict(var, value, assignment) == False: 
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    csp.nodes_counter += 1
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
                csp.unassign(var, assignment)
        return None
    
    result = backtrack({})
    print "Nodes expanded: ", csp.nodes_counter 
    if ( inference == forward_checking ):  
        print "Consistency checks: ", csp.has_conflict_calls
    elif ( inference == mac ):
        print "Consistency checks: ", csp.has_conflict_calls + csp.arc_conflict_calls
    else:
        print "Consistency checks: ", csp.has_conflict_calls
    return result
    
    

# Min-conflicts search
def min_conflicts(csp, max_steps=100000):
    "Solve a CSP by stochastic hillclimbing on the number of conflicts."
    
    def min_conflicts_value(csp, var, current):
        "Return the value that will give var the least number of conflicts."
        "If there is a tie, choose at random."
        
        return argmin_random_tie(csp.domains[var],
                                 lambda val: csp.nconflicts(var, val, current))                             
    "Generate a complete assignment for all vars (probably with conflicts)"
    csp.current = current = {}
    for var in csp.vars:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
        csp.nodes_counter  += 1
    "Now repeatedly choose a random conflicted variable and change it"
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            print "Nodes expanded: ", csp.nodes_counter 
            print "Consistency checks: ", csp.nconflicts_calls + csp.has_conflict_calls
            return current
        var = random.choice(conflicted)        
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
        csp.nodes_counter  += 1
    return None


