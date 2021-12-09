from copy import deepcopy
from auxiliary_structures import *


class LR1_Parser:
    def fit(self, start, terms, non_terms, rules_list):
        self.check_input_accuracy(start, terms, non_terms, rules_list)
        self.table = dict()
        self.terms = terms
        self.non_terms = non_terms
        self.non_terms.append("&")
        self.rules = dict()
        self.Buildrules(start, list(rules_list))
        self.first = dict()
        self.Build_first()
        self.vertices = dict()
        self.stack = []
        item = state("&", start, 0, {"$"}, 0)
        self.vertices[0] = Vertex(self.build_closure(item))
        self.stack.append([self.vertices[0], 0])
        while self.stack:
            self.action(self.stack[0][0], self.stack[0][1])
            self.stack.pop(0)
        self.Build_table()

    def Build_first(self):
        for sym in self.non_terms:
            self.first[sym] = set()
        for sym in self.non_terms:
            checked = []
            self.set_first(sym, sym, checked)

    def set_first(self, f_sym, cur_sym, checked):
        if cur_sym in self.terms:
            self.first[f_sym].add(cur_sym)
        elif cur_sym in self.non_terms:
            for rule in self.rules[cur_sym]:
                if rule in checked:
                    return
                checked.append(rule)
                self.set_first(f_sym, rule.right[0] if rule.right else "", checked)

    def check_input_accuracy(self, start, terms, non_terms, rules_list):
        if start not in non_terms:
            raise RuntimeError("Start must be non-terminal symbol.")
        if len(set(non_terms) & set(terms)) != 0:
            raise RuntimeError(
                "Set of terminal and non-terminal symbols should not intersect."
            )
        for rule in rules_list:
            rule_ = list(rule.split("->"))
            if len(rule_) != 2:
                raise RuntimeError(
                    "Rules should consist from two parts, divided by '->' symbol"
                )
            if len(rule_[0]) != 1:
                raise RuntimeError("LHS of rule shoud be one symbol")
            if rule_[0] not in non_terms:
                raise RuntimeError("Rules should start with non-terminal symbol")
            for char in rule_[1]:
                if char not in non_terms and char not in terms:
                    raise RuntimeError(f"Symbol '{char}' is not in symbols list.")

    def Buildrules(self, start, rules_list):
        for i in self.non_terms:
            self.rules[i] = set()
        for i in range(len(rules_list)):
            rule = Rule(i + 1, *rules_list[i].split("->"))
            self.rules[rule.left].add(rule)
        self.rules["&"].add(Rule(0, "&", start))

    def build_closure(self, item):
        States = dict()
        States["done"] = set()
        States["todo"] = set()
        States["todo"].add(item)
        while States["todo"]:
            current_state = States["todo"].pop()
            if current_state in States["done"]:
                continue
            if current_state.dot_val in self.terms or current_state.dot_val == "":
                States["done"].add(current_state)
                continue
            for rule in self.rules[current_state.dot_val]:

                if current_state.is_last:
                    States["todo"].add(
                        state(rule.left, rule.right, 0, current_state.follow, rule.id)
                    )
                else:
                    if current_state.next_sym() in self.non_terms:
                        States["todo"].add(
                            state(
                                rule.left,
                                rule.right,
                                0,
                                self.first[current_state.next_sym()],
                                rule.id,
                            )
                        )
                    else:
                        States["todo"].add(
                            state(
                                rule.left,
                                rule.right,
                                0,
                                {current_state.next_sym()},
                                rule.id,
                            )
                        )
            States["done"].add(current_state)
        return States["done"]

    def action(self, vertex, parent_ind):
        v1 = deepcopy(vertex)
        for term in self.terms:
            new_states = set()
            for state in v1.states:
                if state.dot_val == term:
                    new_states.update(self.build_closure(state.move_dot()))
            if new_states:
                if Vertex(new_states) not in self.vertices.values():
                    self.vertices[parent_ind].routines[term] = len(self.vertices)
                    self.vertices[len(self.vertices)] = Vertex(new_states)
                    self.stack.append(
                        [self.vertices[len(self.vertices) - 1], len(self.vertices) - 1]
                    )
                else:
                    self.vertices[parent_ind].routines[term] = get_key(
                        Vertex(new_states), self.vertices
                    )
        v2 = deepcopy(vertex)
        for nterm in self.non_terms:
            new_states = set()
            for state in v2.states:
                if state.dot_val == nterm:
                    new_states.update(self.build_closure(state.move_dot()))
            if new_states:
                if Vertex(new_states) not in self.vertices.values():
                    self.vertices[parent_ind].routines[nterm] = len(self.vertices)
                    self.vertices[len(self.vertices)] = Vertex(new_states)
                    self.stack.append(
                        [self.vertices[len(self.vertices) - 1], len(self.vertices) - 1]
                    )
                else:
                    self.vertices[parent_ind].routines[nterm] = get_key(
                        Vertex(new_states), self.vertices
                    )
        v3 = deepcopy(vertex)
        for state in v3.states:
            if state.is_empty():
                self.vertices[parent_ind].empties.add(state)

    def Build_table(self):
        for key, value in self.vertices.items():
            self.table[key] = dict()
            if value.routines:
                self.table[key] = value.routines
        for key, value in self.vertices.items():
            for empty in value.empties:
                for r in empty.follow:
                    if (
                        r in self.table[key].keys()
                        and self.table[key][r] != f"r{empty.id}"
                    ):
                        raise RuntimeError("Conflict, grammar is not LR(1).")
                    self.table[key][r] = f"r{empty.id}"

    def predict(self, word):
        stack = [0]
        word = word + "$"
        for letter in word:
            while True:
                row = stack[-1]
                row = int(row)
                if not letter in self.table[row].keys():
                    return False
                dest = str(self.table[row][letter])
                if (dest, letter) == ("r0", "$"):
                    return True
                if dest.isdigit():
                    stack.append(letter)
                    stack.append(dest)
                    break
                destid = int(dest[1:])
                reduce_items = list(get_rule_by_id(self.rules, destid).right)
                if reduce_items:
                    if len(stack) <= len(reduce_items) * 2:
                        return False
                    reduce_stack_part = []
                    for i in range(-len(reduce_items) * 2, 0, 2):
                        reduce_stack_part.append(stack[i])
                    if reduce_stack_part != reduce_items:
                        return False
                    stack = stack[: -(len(reduce_items) * 2)]
                rule_left = get_rule_by_id(self.rules, destid).left
                current_row = int(stack[-1])
                if not str(self.table[current_row][rule_left]):
                    return False
                stack.append(rule_left)
                stack.append(str(self.table[current_row][rule_left]))
        return False
