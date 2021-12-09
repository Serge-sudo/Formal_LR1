from copy import deepcopy


class Rule:
    def __init__(self, id, left, right):
        self.id = id
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.id) + ":" + self.left + ":" + self.right


class state:
    def __init__(self, left, right, dot_pos, follow, id):
        self.id = id
        self.left = left
        self.right = right
        self.dot_pos = dot_pos
        self.follow = follow
        self.dot_val = (
            self.right[self.dot_pos] if self.dot_pos < len(self.right) else ""
        )
        self.is_last = 1 if self.dot_pos >= max(len(self.right) - 1, 0) else 0

    def move_dot(self):
        return state(
            self.left,
            self.right,
            min(self.dot_pos + 1, len(self.right)),
            self.follow,
            self.id,
        )

    def next_sym(self):
        return self.right[self.dot_pos + 1]

    def is_empty(self):
        return self.dot_pos == len(self.right)

    def __hash__(self):
        return hash(
            self.left
            + "->"
            + self.right[: self.dot_pos]
            + "."
            + self.right[self.dot_pos :]
            + ","
            + str(self.follow)
        )

    def __eq__(self, other):
        if (
            self.left == other.left
            and self.right == other.right
            and self.dot_pos == other.dot_pos
            and self.follow == other.follow
            and self.dot_val == other.dot_val
            and self.is_last == other.is_last
        ):
            return True
        else:
            return False

    def __repr__(self):
        return (
            self.left
            + "->"
            + self.right[: self.dot_pos]
            + "."
            + self.right[self.dot_pos :]
            + ","
            + str(self.follow)
        )


class Vertex:
    def __init__(self, states):
        self.states = states
        self.routines = dict()
        self.empties = set()

    def __repr__(self):
        return (
            "("
            + str(self.states)
            + ":"
            + str(self.routines)
            + ":"
            + str(self.empties)
            + ")"
        )

    def __hash__(self):
        return hash("(" + str(self.states) + ":" + str(self.routines) + ")")

    def __eq__(self, other):
        if self.states == other.states:
            return True
        else:
            return False


def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


def get_rule_by_id(rules, id):
    for rule_list in rules.values():
        for rule in rule_list:
            if rule.id == id:
                return rule


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


if __name__ == "__main__":
    N_cnt, SIGMA_cnt, P_cnt = [int(i) for i in input().split()]
    non_terms = list(input())
    terms = list(input())
    Rules = set()
    for i in range(P_cnt):
        Rules.add(input())
    start = input()
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    check_cnt = int(input())
    for i in range(check_cnt):
        word = input()
        print("Yes" if LR.predict(word) else "No")
