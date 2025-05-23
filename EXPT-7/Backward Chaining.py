class Rule:
    def __init__(self, conclusion, conditions):
        self.conclusion = conclusion
        self.conditions = conditions

    def __str__(self):
        if not self.conditions:
            return f"THEN {self.conclusion}"
        return f"IF {' AND '.join(self.conditions)} THEN {self.conclusion}"

class KnowledgeBase:
    def __init__(self):
        self.facts = {}
        self.rules = []

    def add_fact(self, name, value):
        if not isinstance(value, bool):
            raise ValueError("Fact value must be a boolean (True or False).")
        self.facts[name] = value
        print(f"Fact added: {name} is {value}")

    def add_rule(self, conclusion, conditions):
        if not isinstance(conditions, list):
            raise ValueError("Conditions must be a list of strings.")
        rule = Rule(conclusion, conditions)
        self.rules.append(rule)
        print(f"Rule added: {rule}")

    def display_facts(self):
        print("\n--- Current Facts ---")
        if not self.facts:
            print("No facts defined.")
            return
        for fact, value in self.facts.items():
            print(f"- {fact}: {value}")

    def display_rules(self):
        print("\n--- Current Rules ---")
        if not self.rules:
            print("No rules defined.")
            return
        for i, rule in enumerate(self.rules):
            print(f"- Rule {i+1}: {rule}")

    def backward_chain(self, goal, _being_proved=None):
        if _being_proved is None:
            _being_proved = set()

        if goal in self.facts:
            return self.facts[goal]

        if goal in _being_proved:
            return False

        _being_proved.add(goal)

        for rule in self.rules:
            if rule.conclusion == goal:
                all_conditions_true = True
                if not rule.conditions:
                    pass

                for condition in rule.conditions:
                    if not self.backward_chain(condition, _being_proved):
                        all_conditions_true = False
                        break

                if all_conditions_true:
                    _being_proved.remove(goal)
                    return True

        _being_proved.remove(goal)
        return False

def get_user_facts(kb):
    print("\n--- Enter Facts ---")
    while True:
        try:
            num_facts = int(input("How many facts do you want to enter? (Enter 0 if none): "))
            if num_facts < 0:
                print("Number of facts cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    for i in range(num_facts):
        while True:
            fact_name = input(f"Enter name for fact #{i+1}: ").strip().lower()
            if not fact_name:
                print("Fact name cannot be empty.")
                continue
            if fact_name in kb.facts:
                print(f"Fact '{fact_name}' already exists. Choose a different name or update later if needed.")
                continue
            break
        while True:
            fact_value_str = input(f"Is fact '{fact_name}' true or false? (t/f, true/false, 1/0): ").strip().lower()
            if fact_value_str in ['t', 'true', '1']:
                fact_value = True
                break
            elif fact_value_str in ['f', 'false', '0']:
                fact_value = False
                break
            else:
                print("Invalid input. Please enter 't', 'f', 'true', 'false', '1', or '0'.")
        kb.add_fact(fact_name, fact_value)

def get_user_rules(kb):
    print("\n--- Enter Rules ---")
    while True:
        try:
            num_rules = int(input("How many rules do you want to enter? (Enter 0 if none): "))
            if num_rules < 0:
                print("Number of rules cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    for i in range(num_rules):
        print(f"\nEntering Rule #{i+1}:")
        while True:
            conclusion = input("Enter the conclusion of the rule (e.g., 'd'): ").strip().lower()
            if not conclusion:
                print("Conclusion cannot be empty.")
                continue
            break
        while True:
            conditions_str = input("Enter the conditions, separated by commas (e.g., 'a,b' or leave blank if none): ").strip().lower()
            if not conditions_str:
                conditions = []
                break
            conditions = [cond.strip() for cond in conditions_str.split(',') if cond.strip()]
            if not conditions and conditions_str:
                print("Please enter valid condition names or leave blank.")
                continue
            break
        kb.add_rule(conclusion, conditions)

def main():
    kb = KnowledgeBase()

    get_user_facts(kb)
    kb.display_facts()

    get_user_rules(kb)
    kb.display_rules()

    print("\n--- Goal ---")
    while True:
        goal = input("Enter the goal you want to achieve (e.g., 'f'): ").strip().lower()
        if not goal:
            print("Goal cannot be empty.")
            continue
        break

    print(f"\nAttempting to achieve goal: '{goal}'...")
    if kb.backward_chain(goal):
        print(f"\nSUCCESS: The goal '{goal}' can be achieved.")
    else:
        print(f"\nFAILURE: The goal '{goal}' cannot be achieved.")

if __name__ == "__main__":
    main()
    