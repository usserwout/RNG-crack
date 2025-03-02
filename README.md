```markdown
# Truncated RNG Cracker

This project is designed to crack the seed of a Linear Congruential Generator (LCG) using truncated states. The project includes scripts for solving the truncated states, visualizing the results, and fuzzing to find the correct seed. We use the LLL method to solve the equations. You can read about how [lattice basis reduction can find the seed of LCG's](https://github.com/spawnmason/randar-explanation/blob/master/README.md).

## Table of Contents

- [Usage](#usage)
- [Files](#files)
- [Functions](#functions)
- [Examples](#examples)

## Usage

### Solving Truncated States

To solve the truncated states and find the seed, you can use the `solve` function from `RNG_double_skip_x_to_double.py`. This function takes a list of tuples containing the truncated state, the number of bits truncated, and the skip value.

Example:
```python
from RNG_double_skip_x_to_double import solve

data = [(11, 4, 1), (126, 7, 2)]
results, result_type = solve(data)
print(f"States found: {results}")
print(f"Result type: {result_type}")
```

### Fuzzing

The fuzzer.py script is used to fuzz and find the correct seed by iterating through possible seeds and checking if they match the given rewards.

## Files

- RNG_double_skip_x_to_double.py: Contains the main logic for solving the truncated states.
- fuzzer.py: Contains the fuzzing logic to find the correct seed.
- util.py: Contains utility functions for processing input and verifying solutions.
- LCG.py: Contains the implementation of the Linear Congruential Generator (LCG).

## Functions

### RNG_double_skip_x_to_double.py

- `solve(data: List[Tuple[int, int, int]]) -> Tuple[List[int], str]`: Solves the truncated states with adjusted LCG parameters and returns the solution vector and the type of result.

### fuzzer.py

- `make_complete_list(accuracy_bits)`: Creates a complete list of accuracy bits.
- `fuzzer(rewards)`: Fuzzes to find the correct seed based on the given rewards.

### util.py

- `process_input(data)`: Processes the input data.
- `verify_solution(results, data)`: Verifies if the solution matches the given data.

## Examples

### Solving Truncated States

```python
from RNG_double_skip_x_to_double import solve

data = [(11, 4, 1), (126, 7, 2)] # (random number, bit accuracy, skipped steps)
results, result_type = solve(data)
print(f"States found: {results}")
print(f"Result type: {result_type}")
```

