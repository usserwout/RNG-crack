from typing import List, Tuple

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LCG import BITS_TOTAL, LCG


# Should return (accurate_bits, bit_accuracy)
def get_bit_accuracy(start: float, end: float) -> int:
    if end == 1: # To ensure we don't get an overflow
      end -= 1e-15
    scaled_value1 = int(start * (1 << 53))
    scaled_value2 = int(end * (1 << 53))
    
    xor = scaled_value1 ^ scaled_value2
    bit_accuracy = 0
    while xor > 0:
        xor >>= 1
        bit_accuracy += 1
      
    assert bit_accuracy != -1, f"Incorrect bit_accuracy: {bit_accuracy}"
    return 53 - bit_accuracy

def get_upper_bits(value: float, bits: int) -> int:
    scaled_value = int(value * (1 << 53))
    return (scaled_value >> (53 - bits)) & ((1 << bits) - 1)



def verify_solution(solution, input_data):
    """Verify if a solution satisfies the lattice equation."""
    rng = LCG(solution[0])
    rng.next_int()
    # element = input_data[index+1]
    # d = rng.next_double_skip(input_data[index][2]-1)
    # print(get_upper_bits(d, element[1]), element[0])
    
    for i in range(0, len(input_data)-1):
        element = input_data[i+1]
        d = rng.next_double_skip(input_data[i][2]-1)
        if get_upper_bits(d, element[1]) != element[0]:
            return False
    return True

    

def java_to_python(n):
    """Convert a Java integer to Python integer"""
    return n if n >= 0 else n + (1<<32)

def python_to_java(n):
    """Convert a Python integer to Java integer"""
    return n if n < (1<<31) else n - (1<<32)

def process_input(data: List[Tuple[int, int]]) -> List[int]:
    return [python_to_java(x) << (BITS_TOTAL - b) for (x, b, _) in data]
