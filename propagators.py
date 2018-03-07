'''
This file will contain different constraint propagators to be used within 
bt_search.

---
A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object---the propagator can use this to get access to the variables 
and constraints of the problem. The assigned variables can be accessed via 
methods, the values assigned can also be accessed.

newly_instantiated_variable is an optional argument. SEE ``PROCESSING REQUIRED''
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs, like so
    (True/False, [(Variable, Value), (Variable, Value) ...]

Propagators will return False if they detect a dead-end. In this case, bt_search 
will backtrack. Propagators will return true if we can continue.

The list of variable value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search NEEDS to know this 
in order to correctly restore these values when it undoes a variable assignment.

Propagators SHOULD NOT prune a value that has already been pruned! Nor should 
they prune a value twice.

---

PROCESSING REQUIRED:
When a propagator is called with newly_instantiated_variable = None:

1. For plain backtracking (where we only check fully instantiated constraints)
we do nothing...return true, []

2. For FC (where we only check constraints with one remaining 
variable) we look for unary constraints of the csp (constraints whose scope 
contains only one variable) and we forward_check these constraints.

3. For GAC we initialize the GAC queue with all constaints of the csp.

When a propagator is called with newly_instantiated_variable = a variable V

1. For plain backtracking we check all constraints with V (see csp method
get_cons_with_var) that are fully assigned.

2. For forward checking we forward check all constraints with V that have one 
unassigned variable left

3. For GAC we initialize the GAC queue with all constraints containing V.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Just 
    check fully instantiated constraints.
    '''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def FCcheck (c, x, pruned):
    for d in x.cur_domain ():
        if not c.has_support (x,d):
            pruned.append ((x,d))
            x.prune_value (d)
    if x.cur_domain_size() == 0:
        return False, pruned
    return True, pruned

def prop_FC(csp, newVar=None):

    pruned = []
    con = []
    
    if newVar == None:
        con = csp.get_all_cons()
    else:
        con = csp.get_cons_with_var(newVar)
                
    for c in con:
        if c.get_n_unasgn() == 1:
            var = c.get_unasgn_vars()[0]
            check, pruned = FCcheck (c, var, pruned)
            if not check:
                return False, pruned
    
    return True, pruned
    
def GAC_Enforce (csp, Q, pruned):
    while Q:
        C = Q.pop (0)
        for V in C.get_scope ():
            if V.is_assigned () == False:
                for d in V.cur_domain ():
                    if not C.has_support (V, d):
                        V.prune_value (d)
                        pruned.append ((V, d))
                        if V.cur_domain_size () == 0:
                            return False, pruned
                        else:  
                            con = csp.get_cons_with_var (V)
                            for c in con:
                                if c not in Q:
                                    Q.append (c)
    return True, pruned
    
    
def prop_GAC(csp, newVar=None):

    pruned = []
    con = []
    
    if newVar == None:
        con = csp.get_all_cons()
    else:
        con = csp.get_cons_with_var(newVar)
        
    check, pruned = GAC_Enforce (csp, con, pruned)
    
    return check, pruned
