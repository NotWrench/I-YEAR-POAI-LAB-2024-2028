class Rule:
    def __init__(self, conclusion, conditions):
        self.conclusion = conclusion
        self.conditions = conditions

    def __str__(self):
        if not self.conditions:
            return f"{self.conclusion}."
        return f"{self.conclusion} :- {', '.join(self.conditions)}."


class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact_name):
        cleaned_fact = fact_name.strip()
        if cleaned_fact:
            self.facts.add(cleaned_fact)

    def get_initial_facts_from_user(self):
        facts_str = input("Enter initial facts (comma-separated, e.g., a,b): ").strip()
        if facts_str:
            for fact in facts_str.split(','):
                self.add_fact(fact)

    def get_rules_from_user(self):
        while True:
            try:
                num_rules_str = input("Enter the number of rules (e.g., 3): ").strip()
                if not num_rules_str:
                    print("No number provided for rules. Assuming 0 rules.")
                    num_rules = 0
                    break
                num_rules = int(num_rules_str)
                if num_rules < 0:
                    print("Number of rules cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter an integer for the number of rules.")

        for i in range(num_rules):
            print(f"\nEntering Rule #{i+1}:")
            conclusion = ""
            while not conclusion:
                conclusion = input("  Enter conclusion for the rule (e.g., d): ").strip()
                if not conclusion:
                    print("  Conclusion cannot be empty. Please try again.")

            conditions_str = input(f"  Enter comma-separated conditions for '{conclusion}' (e.g., a,b or leave blank if none): ").strip()
            conditions = []
            if conditions_str:
                conditions = [cond.strip() for cond in conditions_str.split(',') if cond.strip()]

            rule = Rule(conclusion, conditions)
            self.rules.append(rule)
            print(f"  Rule added: {str(rule)}")


    def get_goal_from_user(self):
        goal = ""
        while not goal:
            goal = input("Enter the goal to check (e.g., f): ").strip()
            if not goal:
                print("Goal cannot be empty. Please try again.")
        return goal

    def forward_chain(self, goal):
        inferred_facts = set(self.facts)

        while True:
            newly_inferred_this_iteration = set()
            for rule in self.rules:
                if rule.conclusion not in inferred_facts:
                    all_conditions_met = True
                    for condition in rule.conditions:
                        if condition not in inferred_facts:
                            all_conditions_met = False
                            break

                    if all_conditions_met:
                        newly_inferred_this_iteration.add(rule.conclusion)

            if not newly_inferred_this_iteration:
                break

            inferred_facts.update(newly_inferred_this_iteration)

        return goal in inferred_facts


def main():
    kb = KnowledgeBase()

    print("--- Setup Knowledge Base ---")
    kb.get_initial_facts_from_user()
    kb.get_rules_from_user()
    goal = kb.get_goal_from_user()

    print("\n--- Knowledge Base Summary ---")
    if kb.facts:
        print(f"Initial Facts: {', '.join(sorted(list(kb.facts)))}")
    else:
        print("Initial Facts: None")

    if kb.rules:
        print("Rules:")
        for i, rule_obj in enumerate(kb.rules):
            print(f"  R{i+1}: {str(rule_obj)}")
    else:
        print("Rules: None")
    print(f"Goal: {goal}")

    print("\n--- Running Forward Chaining ---")
    if kb.forward_chain(goal):
        print(f"The goal '{goal}' can be achieved.")
    else:
        print(f"The goal '{goal}' cannot be achieved.")


if __name__ == "__main__":
    main()
