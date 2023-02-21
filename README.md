
# LR(1)

Launch:

python3 main.py

Launch tests:

py.test --cov=lr tests/

***************************
build_closure - pushes state into stack, than takes items form stack one by one...if dot_val is non-termianl, it addes all the rules which contain that letter in Left hand side into stack, than pushes our current state into "done" list.
action - makes edges in our "automaton", it iterates over terms and pushes all states which expect that term into new vertex.Same thing with non-terms. 
For every vertex we have list called empties, that is all the rules whose dot_pos is last.
Build_table - Creates table from "automaton".
predict - uses table to find out if word is in grammar.


