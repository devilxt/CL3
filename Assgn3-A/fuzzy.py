
# 1. FUZZY SET OPERATIONS

def fuzzy_union(A, B):
    """Calculates the Union (max) of two fuzzy sets."""
    elements = set(A.keys()).union(set(B.keys()))
    return {x: max(A.get(x, 0.0), B.get(x, 0.0)) for x in elements}

def fuzzy_intersection(A, B):
    """Calculates the Intersection (min) of two fuzzy sets."""
    elements = set(A.keys()).union(set(B.keys()))
    return {x: min(A.get(x, 0.0), B.get(x, 0.0)) for x in elements}

def fuzzy_complement(A):
    """Calculates the Complement (1 - x) of a fuzzy set."""
    return {x: round(1.0 - val, 2) for x, val in A.items()}

def fuzzy_difference(A, B):
    """Calculates the Difference (A intersection B_complement)."""
    B_comp = fuzzy_complement(B)
    return fuzzy_intersection(A, B_comp)


# 2. FUZZY RELATIONS

def cartesian_product(A, B):
    """Creates a fuzzy relation matrix using the min of individual memberships."""
    A_vals = list(A.values())
    B_vals = list(B.values())
    relation = [[min(u, v) for v in B_vals] for u in A_vals]
    return relation

def max_min_composition(R, S):
    """Performs max-min composition on two fuzzy relation matrices."""
    rows_R = len(R)
    cols_R = len(R[0])
    cols_S = len(S[0])
    
    result = [[0.0] * cols_S for _ in range(rows_R)]
    
    for i in range(rows_R):
        for j in range(cols_S):
            result[i][j] = max(min(R[i][k], S[k][j]) for k in range(cols_R))
            
    return result

# TESTING THE IMPLEMENTATION

if __name__ == "__main__":
    Set_A = {'x1': 0.2, 'x2': 0.5, 'x3': 0.8}
    Set_B = {'x1': 0.4, 'x2': 0.7, 'x3': 0.3}

    print("--- Fuzzy Set Operations ---")
    print(f"Set A: {Set_A}")
    print(f"Set B: {Set_B}")
    print(f"Union (A U B):       {fuzzy_union(Set_A, Set_B)}")
    print(f"Intersection (A ∩ B):{fuzzy_intersection(Set_A, Set_B)}")
    print(f"Complement (A'):     {fuzzy_complement(Set_A)}")
    print(f"Difference (A \ B):  {fuzzy_difference(Set_A, Set_B)}")

    print("\n--- Fuzzy Relations ---")
    Set_C = {'y1': 0.6, 'y2': 0.9}
    
    relation_R = cartesian_product(Set_A, Set_C)
    print("Cartesian Product (Set A x Set C) -> Matrix R:")
    for row in relation_R:
        print(row)

    relation_S = [[0.5, 0.8], 
                  [0.4, 0.7]]
                  
    print("\nDummy Matrix S:")
    for row in relation_S:
        print(row)
        
    composition_result = max_min_composition(relation_R, relation_S)
    print("\nMax-Min Composition (R o S):")
    for row in composition_result:
        print(row)