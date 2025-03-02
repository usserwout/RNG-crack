
from Crate import load_crate_from_file
import os
import sys
import json
from util import get_bit_accuracy, get_upper_bits
from stats import print_list_frequencies

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RNG_double_skip_x_to_double import solve
from LCG import LCG

def load_crate_rewards():
    with open('./simulate/data/crateRewardsGod2.json', 'r') as file:
        data = json.load(file)
    flattened_data = [item for sublist in data for item in sublist]
    return flattened_data



def get_acc_bits(reward_list, crate):
    accuracy_bits = []
    skip = 1
    for reward in reward_list:
        interv = crate.intervals[reward]
        bit_acc = get_bit_accuracy(interv[0] / crate.total , interv[1] / crate.total) 
        if bit_acc >= 4 :
            if len(accuracy_bits) > 0:
                accuracy_bits[-1] = (accuracy_bits[-1][0], accuracy_bits[-1][1], skip)
            accuracy_bits.append((get_upper_bits(interv[1]/crate.total, bit_acc), bit_acc, None))
            skip = 1
        else:
            skip += 1
    assert len(accuracy_bits) > 0, "No data points generated"
    accuracy_bits[-1] = (accuracy_bits[-1][0], accuracy_bits[-1][1], skip)
    
    return accuracy_bits


def _crack(accuracy_bits):
    print_list_frequencies([b for (a,b,c) in accuracy_bits])
    print(accuracy_bits)
    
     
    # Solve the truncated states
    results = solve(accuracy_bits)
    if len(results) == 0:
        print("No solution found")
        return None
    
    cracked_crate = load_crate_from_file('./simulate/data/crateDataGod.json', results[-1])
    cracked_crate.next_int()
    
    for i in range(accuracy_bits[-1][2]-1):
        cracked_crate.next_double()
    return cracked_crate

def crack(reward_list, crate):
    accuracy_bits = get_acc_bits(reward_list, crate)
    return _crack(accuracy_bits)
    
    
    
    

def crack_crate(rewards):
    input_size = 250
    ultra_crate = load_crate_from_file('./simulate/data/crateDataGod.json', 73498798 ^0x5DEECE66D)
    crate = crack(rewards[20:input_size], ultra_crate)
    if crate is None:
        print("Failed to crack crate")
        return
    correct = True
    for i in range(10):
        next_reward = crate.next()
        print(f"{next_reward:<25} {rewards[input_size + i]:<25}")
        correct = correct and next_reward == rewards[input_size + i]
    if correct:
       print("\033[92mCrate cracked successfully\033[0m")
    else:
        print("\033[91mCrate cracked failed\033[0m")
        
    


def crack_simulated_crate():
    crate = load_crate_from_file('./simulate/data/crateDataGod.json', 258885872875019)
    crate.next_int()
    reward_list = []
    for i in range(30):
        reward_list.append(crate.next())
    print(reward_list)

def crack_crate_with_skips():
    crate = load_crate_from_file('./simulate/data/crateDataGod.json', 69 ^0x5DEECE66D)
    
    with open('./simulate/data/crateRewardsGod2.json', 'r') as file:
        data = json.load(file)
    
    all_bits = []
    for i,crate_items in enumerate(data[:-1]):
        crate_bits = get_acc_bits(crate_items, crate)
        if len(all_bits) > 0:
            all_bits[-1] = (all_bits[-1][0], all_bits[-1][1], all_bits[-1][2] - 5)
        print("---------------------------------------------------")
        print(f"Index: {i}")
        if _crack(crate_bits) is not None:
            print("WE HAVE A WINNER!")
            return
        
        all_bits.extend(crate_bits)
    
    
    cracked_crate = _crack(all_bits)
    if cracked_crate is None:
        print("Failed to crack crate")
        return
    
    for i in range(10):
        print(f"{cracked_crate.next():<25} {data[-1][i]:<25}")
        
        
def crack_crate_test():  
    with open('./simulate/data/crateRewardsRare2.json', 'r') as file:
        data = json.load(file)

    for crate_rewards in data:
        crate = load_crate_from_file('./simulate/data/crateDataGod.json', 69 ^0x5DEECE66D)
        print("Index:", data.index(crate_rewards))
        real_crate = crack(crate_rewards, crate)
        if real_crate is None:
            print("Failed to crack crate")
            return
        
        for _ in range(10):
            print(f"{real_crate.next():<25} {crate.next():<25}")
        print("---------------------------------------------------")
    



if __name__ == '__main__':
    data = load_crate_rewards()
    crack_crate(data)


    
    