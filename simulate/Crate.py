from collections import OrderedDict
from typing import TypeVar, Generic, Dict, Tuple
import json
import sys
import random
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LCG import LCG, DOUBLE_UNIT

E = TypeVar('E')

class Crate(Generic[E]):
    def __init__(self, rng: LCG = None):
        self.map = OrderedDict()
        self.intervals: Dict[E, Tuple[float, float]] = {}
        self.random = LCG(random.randint(1, (1 << 63) - 1)) if rng is None else rng
        self.total = 0.0

    def add(self, chance: float, obj: E):
        if chance <= 0.0:
            return
        self.total = round(self.total + chance,4)
        assert obj not in self.intervals, "Object already exists in crate: "+str(obj)
        
        assert self.total not in self.map, "Total already exists in crate: "+str(self.total) + " for object: "+str(obj)
        self.map[self.total] = obj
        
        self.intervals[obj] = (round(self.total - chance, 4), self.total)

    def next(self) -> E:
        d = self.random.next_double() * self.total
        for key in self.map:
            if key >= d:
                return self.map[key]
            
    def next_interval(self) -> Tuple[float, float]:
        d = self.random.next_double() * self.total
        for key in self.map:
            if key >= d:
                return self.intervals[self.map[key]]

    def get_crate_item(self, d: float) -> E:
        for key in self.map:
            if key >= d:
                return self.map[key]

    def next_int(self) -> int:
        return self.random.next_int()
    
    def set_seed(self, seed: int):
        self.random = LCG(seed)
        

    def next_double(self) -> float:
        return self.random.next_double()

    def destroy(self):
        self.random = None
        self.map.clear()
        self.total = 0.0

    def size(self) -> int:
        return len(self.map)
    

def load_crate_from_file(path: str, seed:int = None, sort_func = None) -> Crate[str]:
    with open(path, 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    crate = Crate[str](None if seed is None else LCG(seed))

    #random.shuffle(data['items'])
    data_list = [(item['chance'], item['name']) for item in data['items']]
    if sort_func is not None:
        data_list = sort_func(data_list)

    # sort by chance
    #data_list.sort(key=lambda x: x[0], reverse=True)
    
    # Reverse order
    #data_list.reverse()
    
    # sort by name
    #data_list.sort(key=lambda x: x[1], reverse=True)
    # sort by chance and name
    #data_list.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    for (chance,name) in data_list:
        crate.add(chance, name)
    return crate