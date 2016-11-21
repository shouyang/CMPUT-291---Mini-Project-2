# CMPUT 291 - Mini Project 2
# Author: Daniel Zhou
# November 2016
import itertools
#===============================================================================

def closure(R,F):
    old = set(R)
    count = 0
    while True: # Used to ensure an encompassing search
        for i in F:
            LHS = set(i[0])
            RHS = set(i[1])
            if LHS.issubset(old) and not RHS.issubset(old):
                old = old.union(RHS)
                count = 0
            else:
                count += 1
        if count > 1*len(F): # By setting count = 0 and breaking once count is higher than the length we ensure that each addition can be compared to each other element.
            break
    return old # old is a set, this set is the elements entailed from R

#def recursive_check(LHS,F): ### NOT USED
    #LHS = LHS
    #LHS_closure = closure(LHS,F)
    ## Get Combinations of LHS
    #LHS_combins = itertools.combinations(LHS, len(LHS)-1)
    #LHS = set(LHS)
    ## Determine if there is a subset of LHS that has the same closure
    #for combin in LHS_combins:
        #LHS_alt = set(combin)
        #LHS_alt_closure = closure(LHS_alt, F)
        
        ## Adjustment: Handles with LHS and Alt closure differs by something in the X of X -> Y
        #diff = LHS.difference(LHS_alt)
        
        ## If an alternative is found, return FD list or continue recursion.
        #if (LHS_alt_closure == LHS_closure) or (LHS_alt_closure.union(diff) == LHS_closure):
            ## Remove all of the old LHS entries from the FD set
            #for FD in F:
                #if set(FD[0]) == set(LHS):
                    #F.append( (combin, FD[1]) )
                    #F.pop ( F.index(FD) )            
            ## Stop condition of Recursion, LHS is simply one varable.
            #if len(LHS) == 1:
                #return (F)
            #else:
                #if recursive_check(LHS_alt,F):
                    #return recursive_check(LHS_alt,F)
                #else:
                    #return (F)
        ## Else try another combination-alternative.
        #else:
            #continue
    ## Only hit when no alt has been found.
    #return (F)

    
def check_redundancy( LHS, RHS , T):
    # Recursion Guard
    if len(LHS) > 1:
        LHS_combins = itertools.combinations(LHS, len(LHS)-1)
        # For each sub combination of the LHS, try see if RHS is in the closure
        for combin in LHS_combins:
            combin_closure = closure(combin,T)

            # If so, remove the (LHS,RHS) dependecy and replace with (alt,RHS)
            if set(RHS).issubset(combin_closure):
                # Case 1: Continue with recursion, see if there is a smaller step.
                T.pop ( T.index( (LHS,RHS) ) )
                T.append ( (''.join(combin),RHS) )
                return check_redundancy(combin, RHS, T)
        return T
    else:    
        return T # T is either a modified or original version of the FD list.
    
    
def min_closure(F):
    # Step 1 - Make all FDs into X -> Y where Y is only 1 element
    F_ = [] # Temp List
    for FD in F:
        if len(FD[1]) == 1:
            F_.append(FD)
        else:
            for i in range(0,len(FD)):
                F_.append( (FD[0], FD[1][i]) )
                
    F = F_
    # Step 2
    count = 0
    while True: # Loop ensures all elements are checked against all elements.
        F_ = check_redundancy( F[0][0], F[0][1], F)
        if set(F) != set(F_): # Case: FD had redundant variable, removed.
            F = F_
            count = 0 # Count reset since now, we need to recheck this to everything else.
        else:
            F.append(F.pop(0) ) # Case: No changes, cycle front element to end.
            count += 1
        
        if count > 3*len(F): # Break Condition
            break
    # Step 3
    count = 0
    while True: # Loop ensures all elements are checked against all elements.
        FD = F[0]
        LHS = FD[0]
        
        # Check if closure is the same for a given X in X -> Y, without this FD.
        LHS_closure = closure(LHS,F)
        F.pop(0)
        LHS_closure_alt = closure(LHS,F)
        
        # If so, do not add back the FD. 
        if LHS_closure == LHS_closure_alt:
            count = 0
        # Otherwise do so.
        else: 
            F.append(FD)
            count += 1
            
        if count > 2* len(F): # Break Condition.
            break
    return F # F is a list of the functional dependencies that ensure minimal cover.
    
        
        
#T = [("ABH","CK"),("A","D"),("C","E"),("BGH","F"),("F","AD"),("E","F"),("BH","E")]

## T @ Step 2 = [('BH', 'F'), ('F', 'A'), ('F', 'D'), ('E', 'F'), ('BH', 'E'), ('BH', 'C'), ('BH', 'K'), ('A', 'D'), ('C', 'E')]

#print ( min_closure(T) )



