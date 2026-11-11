from pathlib import Path

class Term:
    def __init__(self, name, involved, num1, literals):
        self.name = name
        if type(involved) == int:
            self.involved = {involved}
        else:
            self.involved = involved
        self.num1 = num1
        self.literals = literals
        self.used = False

def petrick_method(remaining_pi, not_covered):
    clauses = []
    for term in not_covered:
        clause = set()
        for i, pi in enumerate(remaining_pi):
            if term in pi.involved:
                clause.add(i)
        clauses.append(clause)

    curr_sop = [{index} for index in clauses[0]]

    for next_clause in clauses[1:]:
        next_sop = []
        for term_set in curr_sop:
            for literal in next_clause:
                new_set = term_set.copy()
                new_set.add(literal)
                if new_set not in next_sop:
                    next_sop.append(new_set)

        filtered_sop = []
        for s1 in next_sop:
            absorved = False
            for s2 in next_sop:
                if s1 != s2 and s2.issubset(s1):
                    absorved = True
                    break
            if s1 not in filtered_sop and not absorved:
                filtered_sop.append(s1)

        curr_sop = filtered_sop

    best_combination = min(curr_sop, key=lambda s: (len(s), sum(remaining_pi[index].literals for index in s)))

    return [remaining_pi[index] for index in best_combination]

def compare(t1, t2):
    index = 0
    diffs = 0
    result = [0] * 4
    for i in range(0, 4):
        result[i] = t1.name[i]
        if t1.name[i] != t2.name[i]:
            diffs += 1
            index = i
    if diffs == 1:
        result[index] = 2
        t1.used = True
        t2.used = True
        return result
    return None

def format_pi(pi):
    pi_str = ""
    if pi.name[0] == 1:
        pi_str += "A"
    elif pi.name[0] == 0:
        pi_str += "!A"
    if pi.name[1] == 1:
        pi_str += "B"
    elif pi.name[1] == 0:
        pi_str += "!B"
    if pi.name[2] == 1:
        pi_str += "C"
    elif pi.name[2] == 0:
        pi_str += "!C"
    if pi.name[3] == 1:
        pi_str += "D"
    elif pi.name[3] == 0:
        pi_str += "!D"
    return pi_str

def format_answer(answer):
    return " + ".join([format_pi(pi) for pi in answer])

def minimize(equation):
    minterms = [term.strip() for term in equation.split("+")]
    val = 1
    count = 0
    group0 = []
    group1 = []
    group2 = []
    group3 = []
    group4 = []

    for term in minterms:
        num1 = 4
        result = [0] * 4
        for char in term:
            if char == "!":
                num1 -= 1
                val = 0
            elif char == "A":
                result[0] = val
                val = 1
            elif char == "B":
                result[1] = val
                val = 1
            elif char == "C":
                result[2] = val
                val = 1
            elif char == "D":
                result[3] = val
                val = 1
        t = Term(result, count, num1, 4)
        count += 1

        if num1 == 0:
            group0.append(t)
        elif num1 == 1:
            group1.append(t)
        elif num1 == 2:
            group2.append(t)
        elif num1 == 3:
            group3.append(t)
        else:
            group4.append(t)

    prime_implicants = []
    while True:
        new_group0 = []
        new_group1 = []
        new_group2 = []
        new_group3 = []
        new_group4 = []
        combined = False

        for t1 in group0:
            for t2 in group1:
                test = compare(t1,t2)
                if test is not None:
                    new_group0.append(Term(test, t1.involved | t2.involved, 0, t1.literals - 1))
                    combined = True
        for t1 in group1:
            for t2 in group2:
                test = compare(t1,t2)
                if test is not None:
                    new_group1.append(Term(test, t1.involved | t2.involved, 1, t1.literals - 1))
                    combined = True
        for t1 in group2:
            for t2 in group3:
                test = compare(t1,t2)
                if test is not None:
                    new_group2.append(Term(test, t1.involved | t2.involved, 2, t1.literals - 1))
                    combined = True
        for t1 in group3:
            for t2 in group4:
                test = compare(t1,t2)
                if test is not None:
                    new_group3.append(Term(test, t1.involved | t2.involved, 3, t1.literals - 1))
                    combined = True

        for t in group0:
            if t.used == False:
                prime_implicants.append(t)
        for t in group1:
            if t.used == False:
                prime_implicants.append(t)
        for t in group2:
            if t.used == False:
                prime_implicants.append(t)
        for t in group3:
            if t.used == False:
                prime_implicants.append(t)
        for t in group4:
            if t.used == False:
                prime_implicants.append(t)

        if combined == False:
            break

        group0 = new_group0.copy()
        group1 = new_group1.copy()
        group2 = new_group2.copy()
        group3 = new_group3.copy()
        group4 = new_group4.copy()

    unique_pi = []
    for pi in prime_implicants:
        if pi.involved not in [u.involved for u in unique_pi]:
            unique_pi.append(pi)
    prime_implicants = unique_pi

    cover_table = [[0 for _ in range(0, count)] for _ in prime_implicants]
    for i, pi in enumerate(prime_implicants):
        for term in pi.involved:
            cover_table[i][term] = 1

    final_answer = set()
    epi_rows = set()
    not_covered = [i for i in range(0, count)]
    x_num = 0
    row = 0
    for j in range(0, count):
        for i in range(0, len(prime_implicants)):
            if cover_table[i][j] == 1:
                x_num += 1
                row = i
        if x_num == 1:
            final_answer.add(prime_implicants[row])
            epi_rows.add(row)
            for term in prime_implicants[row].involved:
                if term in not_covered:
                    not_covered.remove(term)
        x_num = 0

    if not_covered:
        remaining_pi = [pi for i, pi in enumerate(prime_implicants) if i not in epi_rows]
        petrick_choice = petrick_method(remaining_pi, not_covered)

        for pi in petrick_choice:
            final_answer.add(pi)

    print(f"{format_answer(final_answer)} / {sum(pi.literals for pi in final_answer)} literais")

curr_dir = Path(__file__).resolve().parent
txt_path = curr_dir / "equations.txt"

with open(txt_path, "r", encoding="utf-8") as entrada:
    for linha in entrada:
        minimize(linha)