from main import _crack,get_acc_bits
from Crate import load_crate_from_file
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RNG_double_skip_x_to_double import solve


def make_complete_list(accuracy_bits):
  # Count from 10 to 3
  frequenties = [[] for _ in range(10)]
  for i,acc in enumerate(accuracy_bits):
    frequenties[acc[1]].append((i, acc))
  
  arr = [] # (index, original bit_accuracy, (upper_bits, 7, skips))
  for i in range(9, 3, -1):
    
    for (index,freq) in frequenties[i]:
      bits_to_find = max(0, 7 - freq[1])
      arr.append((index,  bits_to_find,(freq[0] << bits_to_find, max(7, freq[1]), freq[2])))
      
      if len(arr) >= 10:
        break
      
    if len(arr) >= 10:
        break
  # sort array on index
  arr.sort(key=lambda x: x[0])
  # update the skips
  assert len(arr) >= 10, "Not enough data points"
  arr.append(accuracy_bits[-1])
  for i in range(len(arr)-1):
    skip_count = 0
    currEl = arr[i]
    nextEl = arr[i+1]
    
    
    for el in accuracy_bits[currEl[0]:nextEl[0]]:
      skip_count += el[2]
      
    arr[i] = (currEl[0], currEl[1], (currEl[2][0], currEl[2][1], skip_count))
  
  arr.pop()
  return arr
    
    
  
  
  

# 1 + 2*2 + 3*4
# we need 10x 7 bit truncated numbers
def fuzzer(rewards):
  crate = load_crate_from_file('./simulate/data/crateDataGod.json', 11169 ^0x5DEECE66D)
  accuracy_bits = get_acc_bits(rewards, crate)
  accuracy_bits = make_complete_list(accuracy_bits)
  
  amount_bits_to_find =  sum([x[1] for x in accuracy_bits])
  print(accuracy_bits)
  print(f"Checking {1<<amount_bits_to_find} ({amount_bits_to_find} bits) possible seeds")

  num_bits_needed = np.array([x[1] for x in accuracy_bits], dtype=np.int8)
  num_arr = np.array([np.array(x[2], dtype=np.int16) for x in accuracy_bits])
  last_progress = 0
  it = 1<<amount_bits_to_find
  for i in range(it):
    
    
    idx = 0
    overflow = True
    while overflow and idx < len(num_arr):
      b = num_bits_needed[idx]
      if b == 0:
        idx += 1
        # assert idx < len(num_arr), f"The last bit shouldnt be able to overflow. {idx} >= {len(num_arr)}. Iteration: {i}"
        continue
      
      mask = (1 << b) - 1
      updated_bits = (num_arr[idx][0] + 1) & mask
      overflow = updated_bits < (num_arr[idx][0] & mask)
      num_arr[idx][0] = (num_arr[idx][0] & ~mask) | updated_bits
      idx += 1
      # assert idx < len(num_arr), f"The last bit shouldnt be able to overflow. {idx} >= {len(num_arr)}. Iteration: {i}"
      
    result = solve(num_arr)   
    if len(result) > 0:
      print(f"Seed found: {result}")
         
    
    progress = (i + 1) / it
    p = int(progress * 100)
    if last_progress != p:
      print(f"Progress: {p}%")
      last_progress = p
            

# 258885872875019, 272833224857101, 232721182518583, 236634439735369, 190352393860779, 253814918709165, 266474602855041, 237074390241257, 279570624277349, 88727250135481
if __name__ == '__main__':
  rewards = ["+$500,000","Fly Command Voucher","+$500,000","Godly Spawner Case","Key Container","+$750,000","Spawner Container","+$500,000","Key Container","+5000 Mob Coins","+1000 Mob Coins","+$500,000","+2500 Mob Coins","SkyGod Rank Voucher","+125,000 EXP","Legendary Spawner Case","Mysterious Keys GKit Book","+$750,000","+250,000 EXP","+$750,000","+250,000 EXP","Mysterious Spawner GKit Book","+5000 Mob Coins","Mystery Rank Crate","Mysterious Spawner GKit Book","+2500 Mob Coins","SkyChamp Rank Voucher","+5000 Mob Coins","Mysterious Spawner GKit Book","Spawner Container","+2500 Mob Coins","![SkyLord]! Kit Voucher","3x Villager Spawner","+5000 Mob Coins","![SkyVip]! Kit Voucher","3x Villager Spawner","3x SilverFish Spawner","+$750,000","+$500,000","+1000 Mob Coins","+1000 Mob Coins","3x Villager Spawner","+$1,000,000","Armani Special Set"]
  fuzzer(rewards)


