class Unifier:
    def unify(self, x, y, subst=None):
        if subst is None:
            subst = {}
        if x == y:
            return subst
        elif isinstance(x, str) and x.islower():
            return self.unify_var(x, y, subst)
        elif isinstance(y, str) and y.islower():
            return self.unify_var(y, x, subst)
        elif isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y):
                return None
            if not x:
                return subst
            subst_head = self.unify(x[0], y[0], subst)
            if subst_head is None:
                return None
            return self.unify(x[1:], y[1:], subst_head)
        else:
            return None

    def unify_var(self, var, val, subst):
        if var in subst:
            return self.unify(subst[var], val, subst)
        elif isinstance(val, str) and val.islower() and val in subst:
            return self.unify(var, subst[val], subst)

        if self.occurs_check(var, val, subst):
            return None

        subst[var] = val
        return subst

    def occurs_check(self, var, val, subst):
        if var == val:
            return True
        elif isinstance(val, str) and val.islower() and val in subst:
            return self.occurs_check(var, subst[val], subst)
        elif isinstance(val, list):
            return any(self.occurs_check(var, term, subst) for term in val)
        return False


class ResolutionEngine:
    def __init__(self, knowledge_base, query_str):
        self.kb = [frozenset(clause.split()) for clause in knowledge_base if clause.strip()]
        query_literals = query_str.split()
        self.query_negated_clauses = [frozenset([self.negate(lit)]) for lit in query_literals if lit.strip()]

    def negate(self, literal):
        return literal[1:] if literal.startswith('~') else f'~{literal}'

    def resolve(self, c1, c2):
        resolvents = []
        for l1 in c1:
            for l2 in c2:
                if l1 == self.negate(l2): # e.g., l1 is P, l2 is ~P
                    new_clause = (c1.union(c2)) - {l1, l2}
                    resolvents.append(new_clause)
        return resolvents

    def resolution(self):
        clauses = set(self.kb) | set(self.query_negated_clauses)

        if frozenset() in clauses:
            return True

        new = set()
        while True:
            current_clauses_list = list(clauses)
            for i in range(len(current_clauses_list)):
                for j in range(i + 1, len(current_clauses_list)):
                    c1 = current_clauses_list[i]
                    c2 = current_clauses_list[j]
                    resolvents = self.resolve(c1, c2)
                    if frozenset() in resolvents:
                        return True
                    new.update(resolvents)

            if new.issubset(clauses):
                return False
            clauses.update(new)


if __name__ == "__main__":
    kb_clauses = []
    print("Enter Knowledge Base clauses, one per line. Press Enter on an empty line to finish.")
    while True:
        clause_str = input()
        if not clause_str.strip():
            break
        kb_clauses.append(clause_str)

    query_input_str = input("Enter the query (literals separated by space, e.g., R or P Q): ")

    engine = ResolutionEngine(kb_clauses, query_input_str)
    result = engine.resolution()

    if result:
        print("The query is satisfiable.")
    else:
        print("The query is not satisfiable.")
