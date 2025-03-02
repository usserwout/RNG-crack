

# Constants for `java.util.Random`
BITS_TOTAL = 48
a = 0x5DEECE66D
c = 0xB
m = 2**BITS_TOTAL
DOUBLE_UNIT = 1.0 / (1 << 53)  # Equivalent to java's 0x1.0p-53

class LCG:
    """Simple Linear Congruential Generator implementation"""
    def __init__(self, seed):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed
        self.counter = 0

    def next_state(self):
        self.state = (self.a * self.state + self.c) % self.m

    def get_bits(self, n):
        self.next_state()
        return self.state >> (BITS_TOTAL - n)
    
    def next_double(self):
        high_bits = self.get_bits(26)  # Double.PRECISION - 27 = 26
        low_bits = self.get_bits(27)
        return ((high_bits << 27) + low_bits) * DOUBLE_UNIT

    
    def next_double_skip(self, skip):
        for _ in range(skip):
            self.next_double()
        return self.next_double()
    
    def next_int(self):
        return self.get_bits(32)
