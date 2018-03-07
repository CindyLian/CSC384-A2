'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    v = csp.get_all_unasgn_vars()
    max_deg = -1
    max_var = v[0]
    for var in v:
        temp = 0
        con = csp.get_cons_with_var (var)
        for c in cons:
            temp += (con.get_n_unasgn())
        if temp > max_deg:
            max_deg = temp
            max_var = var
    return max_var
    
def ord_mrv(csp):
    v = csp.get_all_unasgn_vars()
    min_var = v[0]
    for var in v:
        if var.domain_size () < min_var.domain_size ():
            min_var = var
    
    return min_var
    
    
def val_lcv(csp, var):
    con = csp.get_cons_with_var (var)
    domain = var.cur_domain ()
    dict = {}
    
    for x in domain:
        pruned = 0
        var.assign (x)
        for c in con:
            scope = c.get_scope ()
            for s in scope:
                if not s.is_assigned ():
                    for v in s.cur_domain ():
                        if not c.has_support (s,v):
                            s.prune_value (v)
                            pruned += 1
        if pruned not in dict:
            dict[pruned] = []
        dict[pruned].append (x)
        var.unassign (x)
    ret = []
    for key in sorted (dict):
        ret.extend (dict[key])
    return ret
        