from sage.all import *
from typing import List, Tuple
from LCG import LCG, BITS_TOTAL, a, c, m



def get_L(k, adjusted_a):
    """Build the lattice matrix with adjusted multiplier."""
    M = matrix([m])
    A = matrix([pow(adjusted_a, i, m) for i in range(1, k)]).T
    I = matrix.identity(k - 1) * -1
    Z = matrix([0] * (k - 1))
    L = block_matrix([[M, Z], [A, I]])
    return L

def java_to_python(n):
    """Convert a Java integer to Python integer"""
    return n if n >= 0 else n + (1<<32)

def python_to_java(n):
    """Convert a Python integer to Java integer"""
    return n if n < (1<<31) else n - (1<<32)

def process_input(data: List[Tuple[int, int]]) -> List[int]:
    return [python_to_java(x) << (BITS_TOTAL - b) for (x, b) in data]

def solve(data):
    """Solve the truncated states in `data` with adjusted LCG parameters."""
    truncated = process_input(data)

    # Adjusted LCG parameters
    adjusted_a = pow(a, 2, m)
    adjusted_c = (c * (a + 1)) % m

    # Compute K with adjusted parameters
    K = [adjusted_c]
    for i in range(1, len(truncated)):
        K.append((K[-1] + adjusted_c * pow(adjusted_a, i, m)) % m)
    K = vector(K)
    
    # Build the lattice with adjusted multiplier
    L = get_L(len(truncated), adjusted_a)

    shifted = [(x - K[i]) % m for i, x in enumerate(truncated)]
    B =  L.LLL()
    sys = vector(shifted)
    sby = B * sys
    ks = vector(round(x) for x in sby / m)
    zs = B.solve_right(ks * m - sby)
    tmp = sys + zs
    results = [(tmp[i] + K[i]) % m for i in range(len(tmp))]
    assert (L * vector(results)) % m == (L * K) % m

    return results

if __name__ == "__main__":
    from colorama import Fore, Style

    truncated = [(12, 4), (58, 6), (14, 4), (26, 5), (6, 3), (1, 5), (0, 4), (0, 4), (0, 4), (14, 4), (0, 4), (14, 4), (14, 4), (0, 4), (6, 3), (0, 4), (1, 1), (26, 5), (27, 5), (3, 2), (12, 4), (0, 3), (26, 5), (14, 4), (3, 2), (0, 4), (0, 4), (0, 4), (58, 6), (3, 2), (1, 1), (0, 4), (26, 5), (0, 4), (0, 3), (6, 3), (1, 1), (0, 4), (0, 4), (0, 4), (955, 10), (3, 2), (1, 5), (26, 5), (58, 6), (3, 2), (14, 4), (1, 5), (14, 4), (27, 5), (49, 6), 
]
    
    print("Total bytes accuracy", sum([b for _, b in truncated]) , "bits")
    print("Length:", len(truncated))
    
    print(f"Truncated states: {Fore.LIGHTGREEN_EX}{truncated}{Style.RESET_ALL}")

    results = solve(truncated)
    print(f"{Fore.LIGHTBLACK_EX}States found: {results}{Style.RESET_ALL}")

    clone = LCG(results[-1])
    clone.next_int() # Skip one to start at the right `next` value

    # Generate next 10 doubles
    guesses = []
    for _ in range(10):
        guesses.append(clone.next_double())

    print(f"Double Guesses: {Fore.LIGHTRED_EX}{guesses}{Style.RESET_ALL}")
    
