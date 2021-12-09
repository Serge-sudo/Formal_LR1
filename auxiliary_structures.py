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
