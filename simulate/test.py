
import random
import sys
import os
from util import get_bit_accuracy, get_upper_bits
from Crate import load_crate_from_file
from stats import  print_list_frequencies
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RNG_double_skip_x_to_double import solve
from LCG import LCG

total_time = 0
def test_double_skip_to_double():
  points = []
  bit_counts = [4] * 27
   
   
  # get random int from 
  rng = LCG(random.randint(0, 0xFFEECE66D)) #25214903848
  bit_count = 4
  
  skips = 1
  for i in range(len(bit_counts)):
    
    # how to get value between 0-4
    randBits = 0 #random.randint(0, 4)
    d = rng.next_double()
    
    if randBits == 0:
      bit_count = bit_counts[i]
      trunc = get_upper_bits(d, bit_count)
      if len(points)> 0:
        points[-1]  = (points[-1][0], points[-1][1], skips)
      points.append((trunc, bit_count, skips))
      skips = 0
    skips += 1
    
  
  
  assert len(points) > 0, "No data points generated"
  points[-1] = (points[-1][0], points[-1][1], skips)
  
  global total_time
  print(points)
  n=1
  start = time.time()
  for i in range(n):
    results = solve(points)
  
  end = time.time()
  print("Time taken: ", end - start)
  print("Average time taken: ", (end - start) / n)
  total_time += end - start

  if len(results) == 0:
    print("No solution found")
    exit(1)
    return None
  
  #print(results)
  rng_cloned = LCG(results[-1])
  rng_cloned.next_int()
  
  next_doubles = [rng.next_double() for i in range(20)]
  print("============================================")
  for i in range(skips - 1):
    # make sure we sync the two generators
    print(next_doubles[i], rng_cloned.next_double())
  
  print("------------------------------------------")
  
  for i in range(10):
    print(next_doubles[i], rng_cloned.next_double())
  
  
  
  
  
def test_crate_intervals():
    crate = load_crate_from_file('./simulate/crateDataUltra.json', 69 ^0x5DEECE66D)
    crate2 = load_crate_from_file('./simulate/crateDataUltra.json', 69 ^0x5DEECE66D)

    
    reward_list = []
    validate_list = []
    skip = 1
    
    for i in range(1000):
      reward = crate.next()
      reward_list.append(reward)
      interval = crate.intervals[reward]
      interval = (interval[0] / crate.total, interval[1] / crate.total)
      dub = crate2.next_double()
      assert interval[0] <= dub <= interval[1], "Double not in interval"
      
      bit_acc = get_bit_accuracy(interval[0], interval[1])
      if bit_acc >= 4:
          if len(validate_list) > 0:
              validate_list[-1] = (*validate_list[-1][0:2], skip)
          validate_list.append((get_upper_bits(dub, bit_acc),bit_acc, None))
          skip = 0
      skip += 1
      
    assert len(validate_list) > 0, "No data points generated"
    validate_list[-1] = (*validate_list[-1][0:2], skip)
              
        
    accuracy_bits = []
    skip = 1
    for reward in reward_list:
        interv = crate.intervals[reward]
        bit_acc = get_bit_accuracy(interv[0] / crate.total , interv[1] / crate.total)
        if bit_acc >= 4:
            if len(accuracy_bits) > 0:
                accuracy_bits[-1] = (accuracy_bits[-1][0], accuracy_bits[-1][1], skip)
            accuracy_bits.append((get_upper_bits(interv[1]/crate.total, bit_acc), bit_acc, None))
            skip = 0
        skip += 1
            
    assert len(accuracy_bits) > 0, "No data points generated"
    accuracy_bits[-1] = (accuracy_bits[-1][0], accuracy_bits[-1][1], skip)
    
    print("accuracy_bits = ", accuracy_bits)
    print("validate_list = ", validate_list)
    assert accuracy_bits == validate_list, "Lists are not equal"
    
    
    print_list_frequencies([b for (a,b,c) in accuracy_bits])
    print(accuracy_bits)
    
     
    # Solve the truncated states
    results = solve(accuracy_bits)
    print(results)
    
    LCG_clone = LCG(results[-1])
    LCG_clone.next_int()
    
    for i in range(skip-1):
        print(LCG_clone.next_double())
    
    print("------------------------------------------")

    for i in range(10):
        print(LCG_clone.next_double(), crate.next_double())
    

def check_chances():
  with open("simulate/data/crateRewardsRare.json") as f:
    data = json.load(f) # List of strings
  total = len(data)
  frequency = {}
  for item in data:
    if item in frequency:
      frequency[item] += 1
    else:
      frequency[item] = 1
      
  for key in frequency:
    frequency[key] /= total
    
    
  
  with open("simulate/data/crateDataGod.json") as f:
    data = json.load(f)["items"]
  total = sum([x["chance"] for x in data])
  
  chances = {}
  
  for item in data:
    chances[item["name"]] = item["chance"] / total
  
  for key in frequency:
    print(f"{key}\t : {frequency[key]*100:.2f}% : {chances[key]*100:.2f}%")
  missing_keys = set(chances.keys()) - set(frequency.keys())
  for key in missing_keys:
    print(f"{key}\t : 0.00% : {chances[key]*100:.2f}%")
  # keys in data that are not in frequency
  


  
if __name__ == "__main__":
  # for i in range(20):
  #   test_double_skip_to_double()
  check_chances()
  #test_crate_intervals()