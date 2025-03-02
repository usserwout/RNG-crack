
from typing import Dict, List, Tuple
from util import get_bit_accuracy
from termcolor import colored
import itertools
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from RNG_double_to_double import solve
# from LCG import LCG


def plot_bit_accuracy(intervals: Dict[str, Tuple[float, float]], total:float) -> List[float]:
    bit_acc = dict() #
    for reward in intervals:
        interv = intervals[reward]
        acc = get_bit_accuracy(interv[0] / total , interv[1] / total)
        if acc == -1:
          print(interv[0] / total , interv[1] / total)
        if acc not in bit_acc:
            bit_acc[acc] = 0
        bit_acc[acc] += 1

    print_frequencies(bit_acc)
    return bit_acc

    

  
    
def print_frequencies(frequencies):
    # Sort the frequencies dictionary by key (label) in ascending order
    sorted_frequencies = dict(sorted(frequencies.items(), key=lambda item: item[0]))
    
    labels = list(sorted_frequencies.keys())
    data = list(sorted_frequencies.values())
    
    # Determine the maximum frequency for scaling
    max_freq = max(data)
    scale = 50 / max_freq  # Scale to fit within 50 characters width

    # Define a list of colors to cycle through
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    color_cycle = itertools.cycle(colors)

    # Create a bar chart using ASCII characters
    for label, freq in zip(labels, data):
        color = next(color_cycle)
        bar = colored('█' * int(freq * scale), color)
        print(f"{label}: {bar} ({freq})")
        
def print_list_frequencies(frequencies: List[int]):
    # convert to dict
    freq_dict = dict()
    for freq in frequencies:
        if freq not in freq_dict:
            freq_dict[freq] = 0
        freq_dict[freq] += 1
    
    total_sum = sum(frequencies)
    print(f"Total bits: {total_sum}")
    
    print_frequencies(freq_dict)       




if __name__ == '__main__':
  pass
  # find_min_bits()
  # for i in range(8, 4, -1):
  #     print(f"Least accurate bit element count for {i} bits: {find_least_accurate_bit_element_count(i)} elements")
  
  #print(has_enough_values( ([8] * 11) + ([3] * 8)))
                                     
    
  
