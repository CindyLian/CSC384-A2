'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
import cspbase

def binary_ne_grid(kenken_grid):
    size = kenken_grid [0][0]
    variables = []
    csp = cspbase.CSP ('binary_ne_grid')
    domain = list(range(1, size+1))
    tuples = []
    
    for x in range (1, size+1):
        variables.append ([])
        for y in range (1, size +1):
            if not x == y:
                tuples.append ((x,y))
            var = cspbase.Variable(str(x)+str(y), domain)
            variables[x-1].append (var)
            csp.add_var (var)
    
    for x in range (0, size):
        for y in range (1, size):
            for z in range (0, y):
                name = str(x+1) + str(z+1) + str(y+1)
                row = cspbase.Constraint ("row " + name, [variables[x][z], variables[x][y]])
                col = cspbase.Constraint ("col " + name, [variables[z][x], variables[y][x]])
                row.add_satisfying_tuples (tuples)
                col.add_satisfying_tuples (tuples) 
                csp.add_constraint (row)
                csp.add_constraint (col)
    return csp, variables

def nary_ad_grid(kenken_grid):
    size = kenken_grid [0][0]
    row = []
    col = []
    csp = cspbase.CSP ('binary_ne_grid')
    domain = list(range(1, size+1))
    tuples = itertools.permutations (domain)
    
    for x in range (1, size+1):
        row.append ([])
        col.append ([])
        for y in range (1, size+1):
            var = cspbase.Variable (str(x) + str(y), domain)
            row[x-1].append (var)
            csp.add_var(row)
            col[y-1].append (cspbase.Variable (str(x) + str(y), domain))
    
    for x in range (0, n):
        r_con = cspbase.Constraint ("row " + str(x+1), row [x])
        c_con = cspbase.Constraint ("col " + str (x+1), col[x])
        r_con.add_satisfying_tuples (tuples)
        c_con.add_satisfying_tuples (tuples)
        csp.add_constraint(r_con)
        csp.add_constraint(c_con)

    return csp, variables

def add (current_sum, values, unassigned, total_sum, domain):
    tuples = []
    
    if (unassigned == 0 and (not current_sum == total_sum)) or current_sum > total_sum:
        return False
    elif unassigned == 0 and current_sum == total_sum:
        return [values]
    
    for d in domain:
        temp = add(current_sum + d, values + [d], unassigned -1, total_sum, domain)
        if temp:
            tuples.extend (temp)
        
    return tuples

def sub (values, unassigned, difference, domain):
    tuples = []
    if unassigned == 0: 
        for i in values: 
            temp = values.copy ()
            temp.remove (i)
            if (i - sum (temp)) == difference:
                return [values]
        return False
    else:
        for d in domain:
            temp = sub (values + [d], unassigned-1, difference, domain)
            if temp:
                tuples.extend (temp)
    return tuples

def div (values, unassigned, quotient, domain):
    tuples = []
    if unassigned == 0: 
        for i in values: 
            temp = values.copy ()
            temp.remove (i)
            result = i
            for j in temp:
                result = result/j
            if result == quotient:
                return [values]
        return False
    else:
        for d in domain:
            temp = div (values + [d], unassigned-1, quotient, domain)
            if temp:
                tuples.extend (temp)
    return tuples    
    
def mul (current_prod, values, unassigned, total_prod, domain):
    tuples = []
    
    if (unassigned == 0 and (not current_prod == total_prod)) or current_prod > total_prod:
        return False
    elif unassigned == 0 and current_prod == total_prod:
        return [values]
    
    for d in domain:
        temp = mul(current_prod * d, values + [d], unassigned -1, total_prod, domain)
        if temp:
            tuples.extend (temp)
        
    return tuples


def kenken_csp_model(kenken_grid):
    csp, variables = binary_ne_grid (kenken_grid)
    size = kenken_grid[0][0]
    domain = list (range(1, size+1))
    
    for i in range (1, len(kenken_grid)):
        cage = kenken_grid[i]
        if len(cage) == 2:
            cons = cspbase.Constraint ("cage " + str(i), [variables [int(str(cage[0])[0])-1][int(str(cage[0])[1])-1]])
            cons.add_satisfying_tuples ([[cage[1]]])
        
        else:
            scope = []
            for v in cage [:-2]:
                scope.append(variables[int(str(v)[0])-1][int(str(v)[1])-1])
            cons = cspbase.Constraint ("cage " + str(i), scope)
            if cage[-1] == 0: #add
                temp = add(0, [], len(cage)-2, cage[-2], domain)
            elif cage[-1] == 1: #subtract
                temp = sub([],len(cage)-2,cage[-2], domain)
            elif cage[-1] == 2: #divide
                temp = div([],len(cage)-2,cage[-2], domain)
            elif cage[-1] == 3: #3, multiply
                temp = mul (1, [], len(cage)-2, cage[-2], domain)

            cons.add_satisfying_tuples(temp)
            
        csp.add_constraint (cons)
    
    return csp, variables
