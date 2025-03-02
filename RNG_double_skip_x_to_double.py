from sage.all import *
from typing import List, Tuple
from LCG import LCG, a, c, m
import matplotlib.pyplot as plt
from simulate.util import process_input, verify_solution




def visualize_vector(vector, title):
    plt.figure(figsize=(10, 5))
    plt.plot(vector, marker='o')
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()
    
def visualize_matrix(matrix, title):
    plt.figure(figsize=(10, 10))
    plt.imshow(matrix, cmap='viridis', interpolation='none')
    plt.colorbar()
    plt.title(title)
    plt.show()

def visualize_lattice_2d(matrix, title):
    plt.figure(figsize=(10, 10))
    for i in range(matrix.nrows()):
        plt.scatter(matrix[i, 0], matrix[i, 1], color='blue')
        plt.text(matrix[i, 0], matrix[i, 1], f'({matrix[i, 0]}, {matrix[i, 1]})', fontsize=9)
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def get_L(k, a_list):
    """Build the lattice matrix with adjusted multiplier."""
    M = matrix([m])
    A = matrix([a_list[i-1] for i in range(1, k)]).T
    I = matrix.identity(k - 1) * -1
    Z = matrix([0] * (k - 1))
    L = block_matrix([[M, Z], [A, I]])
    
    return L


B_cache =dict()
K_cache = dict()

def solve(data: List[Tuple[int, int, int]]) -> List[int]:
    """
    Solve the truncated states in `data` with adjusted LCG parameters.

    Args:
        data: A list of tuples containing the truncated state, the number of bits truncated, and the skip value.
    """
    truncated = process_input(data)
    
    if len(data) not in K_cache:
        a_list = []
        K = vector(ZZ, len(data))
        curr = 0
        for i, (_, __, skip) in enumerate(data):
            steps = skip * 2
            old_curr = curr
            curr += int(steps)
            a_pow = pow(a, curr, m)
            a_list.append(a_pow)

            modulus = m * (a - 1)
            pow_result = pow(a, old_curr, modulus)
            numerator = pow_result - 1
            denominator = a - 1
            geom_sum = (numerator // denominator) % m
            K[i] = (c * geom_sum) % m
        K_cache[len(data)] = (K, a_list)
    else:
        (K, a_list) = K_cache[len(data)]

    # Build the lattice with adjusted multiplier
    if len(truncated) not in B_cache:
        L = get_L(len(truncated), a_list)
        B = L.LLL()
        B_cache[len(truncated)] = B
       
    
    B = B_cache[len(truncated)]
    
    shifted = [(x - K[i]) % m for i, x in enumerate(truncated)]


    sys = vector(shifted)
    sby = B * sys
    ks = vector(round(x) for x in sby / m)
    closest_vector = B.solve_right(ks * m - sby)
    tmp = sys + closest_vector
    results = [(tmp[i] + K[i]) % m for i in range(len(tmp))]

    
    if not verify_solution(results, data):
        return []

    return results


if __name__ == "__main__":
    from colorama import Fore, Style
    # (truncated_bits, bit_accuracy, skips)[]
    truncated = [(11, 4, 1), (126, 7, 2)

]

    

    results = solve(truncated)
    print(f"{Fore.LIGHTBLACK_EX}States found: {results}{Style.RESET_ALL}")

    clone = LCG(results[-1])
    clone.next_int() # Skip one to start at the right `next` value

    # Generate next 10 doubles
    guesses = []
    for _ in range(10):
        guesses.append(clone.next_double())

    print(f"Double Guesses: {Fore.LIGHTRED_EX}{guesses}{Style.RESET_ALL}")
    
