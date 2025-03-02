from sage.all import *
from typing import List, Tuple
from LCG import LCG, BITS_TOTAL, a, c, m


def get_L(k):
    M = matrix([m])
    A = matrix([a**i for i in range(1, k)]).T
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
    """Solve the truncated states in `truncated`, given `bits_known` known bits"""
    truncated = process_input(data)

    K = [c]
    for i in range(1, len(truncated)):
        K.append((K[-1] + c * a**i) % m)
    K = vector(K)
    L = get_L(len(truncated))
    shifted = [(x - K[i]) % m for i, x in enumerate(truncated)] # We do shift to get valid lattice which contains the origin
    B =  L.LLL()
    sys = vector(shifted)
    sby = B * sys
    ks = vector(round(x) for x in sby / m)
    zs = B.solve_right(ks * m - sby)
    tmp = sys + zs
    results = [(tmp[i] + K[i]) % m for i in range(len(tmp))] # We do unshift to get the original values
    assert (L * vector(results)) % m == (L * K) % m # Sanity check

    return results

if __name__ == "__main__":
    from colorama import Fore, Style

    truncated = [(11, 4), (6, 4), (15, 4), (14, 4)#, (15, 4), (7, 4), (8, 4), (8, 4), (2, 4), (14, 4), (12, 4), (5, 4), (4, 4), (5, 4), (14, 4), (6, 4), (9, 4), (4, 4), (10, 4), (10, 4), (11, 4), (12, 4), (3, 4), (15, 4), (5, 4), (8, 4), (5, 4), (8, 4), (13, 4), (9, 4), (9, 4), (15, 4), (6, 4), (11, 4), (4, 4), (1, 4), (2, 4), (0, 4), (13, 4), (4, 4), (9, 4), (4, 4), (6, 4), (5, 4), (9, 4), (1, 4), (3, 4), (13, 4), (12, 4), (12, 4), 
 ]
    
    print("Total bytes accuracy", sum([b for _, b in truncated]) , "bits")
    print("Length:", len(truncated))
    
    print(f"Truncated states: {Fore.LIGHTGREEN_EX}{truncated}{Style.RESET_ALL}")

    results = solve(truncated)
    print(f"{Fore.LIGHTBLACK_EX}States found: {results}{Style.RESET_ALL}")

    clone = LCG(results[-1])

    # Generate next 10 doubles
    guesses = []
    for _ in range(10):
        guesses.append(clone.next_double())

    print(f"Double Guesses: {Fore.LIGHTRED_EX}{guesses}{Style.RESET_ALL}")
    
