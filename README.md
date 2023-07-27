# LR(1) Parsing

To use LR(1) parsing, you can launch the program by running the following command:

```
python3 main.py
```

To launch tests and check the coverage, you can use the following command:

```
py.test --cov=lr tests/
```

LR(1) parsing involves several steps:

## Build Closure

The `build_closure` function is used to push a state into a stack and then take items from the stack one by one. If the `dot_val` is a non-terminal, it adds all the rules which contain that letter in the left-hand side into the stack, and then pushes the current state into the "done" list.

## Action

The `action` function is used to make edges in our "automaton". It iterates over terms and pushes all states which expect that term into a new vertex. The same thing is done with non-terminals. 

For every vertex, we have a list called `empties`, which contains all the rules whose `dot_pos` is at the last position.

## Build Table

The `build_table` function creates a table from the "automaton" built by the `action` function.

## Predict

The `predict` function uses the table to determine whether a word is in the grammar.
