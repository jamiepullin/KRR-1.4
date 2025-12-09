from copy import deepcopy
from KB import facts, rules, terms
from dataStructures import Compound
from functions import ASK, TELL, unify
import dataStructures as ds

class SandboxKB:
    def __init__(self):
        self.facts = deepcopy(facts)
        self.rules = deepcopy(rules)
        self.terms = deepcopy(terms)
        self.lives_in = self.get_term(ds.Atom, "lives_in") #come back here


    def tell(self, fact):
        TELL(fact, self.facts)

    def ask(self, query):
        ASK(query, self.facts, self.rules)

    def ADD(self, fact: ds.Fact):
        if fact not in self.facts:
            self.facts.append(fact)
            print(f"Added fact: {fact}")

    def REMOVE(self, rule: ds.Rule, i:int):
        if i >= len(rule.antecedent):
            return

        target = rule.antecedent[i]
        facts = []
        for fact in self.facts:
            θ = unify(fact.compound, target.compound, {})
            if θ is None:
                facts.append(fact)

            else: print(f"Removed fact matching antecedent[{i}] of rule: {fact}")

        self.facts = facts

    def MODIFY(self, rule: ds.Rule, i: int, attribute: dict):
        if i >= len(rule.antecedent):
            return

        target = rule.antecedent[i]
        target.compound.update(attribute)
        print(f"Modified rule antecedent[{i}] to: {target}")

        for fact in self.facts:
            θ = unify(fact.compound, target.compound, {})
            if θ is not None:
                fact.compound.update(attribute)
                print(f"Modified fact: {fact}")

    def get_term(self, term_type: type, name: str):
        for term in self.terms:
            if isinstance(term, term_type) and term.name == name:
                return term


    def show_wm(self):
        print("Current WM:")
        for f in self.facts:
            print(f)




# Logic Puzzle 1 ----------------

sandbox1 = SandboxKB()

print("Initial scenario: Three people -- Trump, Musk, and KimK -- each live in a different place.")

def possible_residencies(self, person: ds.Atom, place: ds.Atom): #there has to be a better way to get terms
        return ds.Fact(ds.Compound(self.lives_in, [person, place]))




    """
    1. Musk lives in Silicon Valley.
    2. Trump does not live in Hollywood.
    3. KimK does not live in the White House."""