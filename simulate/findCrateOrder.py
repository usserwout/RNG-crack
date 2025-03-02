from main import load_crate_from_file, get_acc_bits
import os
import sys
from stats import print_list_frequencies
from typing import List, Tuple
from util import get_bit_accuracy, get_upper_bits
from stats import print_list_frequencies
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RNG_double_skip_x_to_double import solve
from LCG import LCG


# 4: 17 - 27
# 5: 12 - 15
# 6: 10 - 12
# 7: 10
def find_min_bits():
    crate = load_crate_from_file("./simulate/data/crateDataGod.json")
    reward_list = [crate.next() for _ in range(700)]

    # next_rewards = [crate.next() for _ in range(10)]

    processed = get_acc_bits(reward_list, crate)
    print(processed, len(processed))

    for i in range(10, len(processed)):
        rewards = processed[-i:]
        bit_acc = [b for (_, b, _) in rewards]
        bits = sum([b for (_, b, _) in rewards])
        print(f"Bits: {bits} | i: {i} | Rewards: {bit_acc}")
        result = solve(rewards)
        if len(result) > 0:
            print_list_frequencies(bit_acc)
            return
    print("No solution found")


def find_all_offsets(weights: List[float]) -> List[float]:
    weights_set = set([0])
    # orders = [[0]] # Bit vector that represents the

    for idx, item in enumerate(weights):
        # i = 0
        for weight in list(weights_set):
            s = round(item + weight, 4)
            if s not in weights_set:
                weights_set.add(s)

                # orders.append(orders[i] + 1)
            # i += 1
    # print(sum(orders))
    return list(weights_set)


def run_find_order(crate, reward_list: List[str], item_to_find: str):
    items_to_order_weight = (
        item_to_find,
        round(crate.intervals[item_to_find][1] - crate.intervals[item_to_find][0], 4),
    )  # [(item, round(crate.intervals[item][1] - crate.intervals[item][0], 4)) for item in items_to_order ]

    # print(f"Target interval: ({crate.intervals[item_to_find][0]}, {crate.intervals[item_to_find][1]})")

    weights = [
        round(crate.intervals[item][1] - crate.intervals[item][0], 4)
        for item in crate.intervals
        if item != item_to_find
    ]
    weights = find_all_offsets(weights)
    
    possible_seeds = find_order(
        reward_list, items_to_order_weight, weights, crate.total
    )
    return possible_seeds


def find_order(
    reward_list: List[str],
    items_to_order_weight: List[Tuple[float, str]],
    weights: List[float],
    total: float,
):
    """
    Find the order of the items in the crate

    Args:
      end_intervals: The weights of the items we're searching for
      items_won: The items that we won
      intervals: The intervals of the items that were not

    """
    name, item = items_to_order_weight

    accuracy_bits = []
    skip = 1

    for reward in reward_list:
        if reward == name:
            if len(accuracy_bits) > 0:
                accuracy_bits[-1] = (0, 0, skip)

            accuracy_bits.append((0, 0, None))
            skip = 1
        else:
            skip += 1

    assert len(accuracy_bits) > 0, "No data points generated"
    accuracy_bits[-1] = (0, 0, skip)

    possible_seeds = set([])

    for idx, w in enumerate(weights):
        target_interval = (w, w + item)

        bit_acc = get_bit_accuracy(
            target_interval[0] / total, target_interval[1] / total
        )
        assert bit_acc != -1, f"Incorrect bit_accuracy: {bit_acc}"

        if bit_acc < 4:
            # print(f"Skipping weight {w} due to bit accuracy: {bit_acc}")
            continue

        upper = get_upper_bits(target_interval[1] / total, bit_acc)

        for i, el in enumerate(accuracy_bits):
            accuracy_bits[i] = (upper, bit_acc, el[2])

        results = solve(accuracy_bits)
        if len(results) > 0:
            # print(f"input: {accuracy_bits}")
            # print_list_frequencies([b for (_,b,__) in accuracy_bits])

            rng = LCG(seed=results[-1])
            rng.next_int()
            for i in range(skip - 1):
                rng.next_double()

            print(f"Possible interval: {target_interval} -> {rng.state} ({idx} / {len(weights)})")

            possible_seeds.add(rng.state)

    return list(possible_seeds)


def test_seeds_using_crate(crate, possible_seeds):
    print("possible_seeds=", possible_seeds)

    expected = [crate.next_double() for _ in range(20)]

    for seed in possible_seeds:
        rng = LCG(seed)
        failed = False
        for i in range(20):
            if rng.next_double() != expected[i]:
                failed = True
                break
        if not failed:
            print("SEED FOUND = ", seed)
            return seed
    print("No correct seed found :(")
    return None

def load_crate_rewards():
    with open("./simulate/data/crateRewardsGod.json", 'r') as file:
        json_data = json.loads(file.read())
        
    flatten = [item for sublist in json_data for item in sublist]  
    return flatten

if __name__ == "__main__":
    # find_min_bits()
    crate = load_crate_from_file("./simulate/data/crateDataGod.json", 69 ^ 0x5DEECE66D)
    #reward_list = [crate.next() for _ in range(3058)]
    reward_list = load_crate_rewards()
    print("Reward count: ", len(reward_list))
    
    possible_seeds = run_find_order(crate, reward_list, "Ultimate Spawner Case")
    print("Possble seeds: ", possible_seeds)
    #correct_seed = test_seeds_using_crate(crate, possible_seeds)
