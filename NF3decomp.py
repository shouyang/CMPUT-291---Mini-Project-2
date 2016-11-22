# CMPUT 291 - Mini Project 2
# Author: Daniel Zhou
# November 2016
import itertools
from closure import *
#===============================================================================

# NF3 performs the third normal form decomposition. It requires the list of
# functional dependencies from some source. 
#
# If in the event some attribute is not connected to any functional dependency
# then it is not captured by the function. Presumably these can be added to the
# relation containing the super key
#
# Input Format:
# Functional Dependneces should be converted into the following format.
#   
# For example:
# T = [("ABH","CK"),("A","D"),("C","E"),("BGH","F"),("F","AD"),("E","F"),("BH","E")]
# NF3decomp(T)
# 
# The input is a list containing set elements. These elements are in the for
# (X,Y) where X and Y are the functional dependency X -> Y.
# X and Y should be expressed as a sequence of capitalized strings.
#
# Output Format:
# The output format is similar to the input format. It is a list of sets
# containing the functional dependencies of a sub relation of R
#
# For example:
# T = [('AB', 'CDE'),('C', 'AD'),('D', 'AE'),('B', 'F')]
# NF3decomp(T)
# Returns>>> [('D', 'AE'), ('B', 'F'), ('AB', 'C'), ('C', 'D')]
# As such each of the 4 returned set are to be made into a table.



def NF3decomp(FDependencies):
    # Input Transformation - Get minimum versions of the cover req.
    Dependencies = min_closure(FDependencies)
    print ("Minimal Cover:")
    print ( Dependencies)
    # Output Template
    Output = []
    # For each distinct X collect all elements relating to X. eg. X -> Y X -> Z = X -> YZ
    for i in range(0, len(Dependencies) ):
        # X,Y is the starting dependency comparisons are made to.
        x = set (Dependencies[i][0])  # X comes the "anchor" to which dependencies are collected for.
        y = set (Dependencies[i][1])  # Y becomes the inital set of dependencies related to X.

        for j in range (0, len(Dependencies) ):
            # Xb, Yb is the pair to be compared with.
            xb = set (Dependencies[j][0])
            yb = set (Dependencies[j][1])
            # If X is the same, yet Y != Yb, ie. The dependency isn't the same, combine the pairs.
            if x == xb and y != yb:
                y = y.union(yb)
            else:
                continue
        # At this point, per each unique X, each of the minimal cover dependencies are condensed for a given X.
        # Recoverting back into strings adds order to the list, this order makes redundancy checking difficuilt.
        
        # Things are thus made into lists, and sorted so to maintain an consistent order.
        x = list(x)
        y = list(y)
        
        x.sort()
        y.sort()
        
        # Mend Sets into original format
        x = "".join(x)
        y = "".join(y)
        if (x,y) not in Output: # Duplicate Checker - Note that string comparison incorporates order.
            # The above set -> list -> sorted list, is to remove order for comparison.
            Output.append( (x,y) )
    return Output

# Assumes that each the functional dependencies completely covers all 
# attributes in the relation.
# 
# Finds the superkey for that set of relations. Presumably used once the 
# 3NF Form is found.
# 
# Input Format:
# T = [("ABH","CK"),("A","D"),("C","E"),("BGH","F"),("F","AD"),("E","F"),("BH","E")]
#
# Output Format:
# A the string representation of the X in X->Y, it is drawing from the input
# functional dependencies.
#
# Note: If no superkey is found then nothing is returned, check for this condition.


def Get_SuperKey(FDependencies):
    Attributes = ""
    for FD in FDependencies:
        Attributes += FD[0]
        Attributes += FD[1]
        
    Attributes = set( list(Attributes) )
    
    for FD in FDependencies:
        FD_Closure = closure(FD[0],FDependencies)
        if FD_Closure == Attributes:
            return FD[0]


#T = [('AB', 'CDE'),('C', 'AD'),('D', 'AE'),('B', 'F')]

#print ( NF3decomp(T) )
#E = [("ABH","CK"),("A","D"),("C","E"),("BGH","F"),("F","AD"),("E","F"),("BH","E")]

#print ( NF3decomp(E) )

#print ( Get_SuperKey(T) )
