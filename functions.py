import dataStructures as ds
from dataStructures import Compound


#------------------- PART III.i - UNIFICATION-------------------

def unify(x, y, θ=None):
    if θ is None:
        θ = {} #start with empty substitution set
    print(f"UNIFY called: {repr(x)}, {repr(y)}, θ = {print_theta(θ)}")
    if x == y:
        return θ  # If x and y are the same, the substitution is complete

    elif isinstance(x, ds.Variable):
        return unify_var(x,y,θ)

    elif isinstance(y, ds.Variable):
        return unify_var(y,x,θ)

    elif isinstance(x, ds.Compound) and isinstance(y, ds.Compound):
        if x.op != y.op or len(x.args) != len(y.args):
            return None

        for arg_x, arg_y in zip(x.args, y.args):
            θ = unify(arg_x, arg_y, θ) #recursively unify arguments
            if θ is None:
                return None
        return θ

    return None

def unify_var(var, x, θ):
    print(f"Entering Unify function")
    if var in θ:
        return unify(θ[var], x, θ)

    elif isinstance(x, ds.Variable) and x in θ: #check x binding
        return unify(var, θ[x], θ)

    if occur_check(var, x): # Occur check to prevent circular unifications
        raise Exception("OCCUR-CHECK Error")


    θ[var] = x
    print(f"Added binding: {var.name} / {repr(x)}, θ = {print_theta(θ)}")

    return θ

def occur_check(var, x):
    if var == x:
        return True
    elif isinstance(x, ds.Compound):
        for arg in x.args:
            if occur_check(var, arg):
                return True
    return False


def print_theta(theta):
    return ", ".join(f" {v.name} / {repr(t)}" for v, t in theta)

#------------------- PART III.ii - INFERENCE -------------------
def get_rule_candidates(fact, rules): #return list of rules that match given fact

    candidates = []

    fact_op = fact.compound.op
    print(f"get_rule_candidates: looking for rules matching operator '{fact_op}")

    for rule in rules:
        print(f"Checking rule: {rule}")

        if rule.direction != "forward": #identify forward rules only
            print(" - Skipped: not a forward rule")
            continue

        for conjunct in rule.antecedent:
            if not isinstance(conjunct.compound, Compound):
                print(f" - Skipped: antecedent is not a compound")

            antecedent_op = conjunct.compound.op
            print(f" Antecedent operator: {antecedent_op}")

            if antecedent_op == fact_op:
                print(f" MATCH: Adding rule to candidates")
                candidates.append(rule)
                break
            else: print("No match")

    print(f"\n Final Candidates: {candidates}")
    return candidates

def get_fact_candidates(query, facts):
    candidates = []
    for fact in facts:

        if isinstance(fact, Compound):
            fact_compound = fact  # already a Compound
        else:
            fact_compound = fact.compound  # Fact object


        if fact_compound.op != query.op:
            continue

        if len(fact_compound.args) != len(query.args):
            continue

        candidates.append(fact)
    return candidates




def subst(θ,  term):
    if isinstance(term, ds.Variable):
        for (var, val) in θ:
            if var == term:
                return val
            return term
    elif isinstance(term,Compound):
        return Compound(term.op, [subst(θ, conjunct) for conjunct in term.args])
    else:
        return term

def ADD_FACT(kb, fact):
    if fact not in kb['facts']:
        kb['facts'].append(fact)

def ADD_RULE(kb, rule):
    if rule not in kb['rules']:
        kb['rules'].append(rule)



#TELL (Forward Chaining)
def TELL(fact, KB_facts, KB_rules):
    if fact in KB_facts:
        return

    ADD_FACT({'facts': KB_facts, 'rules': KB_rules}, fact)
    print(f"Added fact: {fact}")

    candidate_rules = get_rule_candidates(fact, KB_rules)

    for rule in candidate_rules:
        for ant in rule.antecedent:
            θ = unify(fact.compound, ant.compound, [])
            if θ is not None:
                cons_subst = subst(θ, rule.consequent.compound)
                new_fact = ds.Fact(cons_subst)
                print(F"new fact derived: {new_fact}")
                TELL(ds.Fact(cons_subst), KB_facts, KB_rules)

#ASK (Backward chaining)
def ASK(query, KB_facts, KB_rules):
    print(f"\nASK called for query: {query.compound}")

    fact_candidates = get_fact_candidates(query.compound, KB_facts)
    for fact in fact_candidates:
        θ = unify(query.compound, fact.compound, {})
        if θ is not None:
            print(f"Fact matched: {fact} binds to θ = {θ}")
            return dict(θ)  # convert list of tuples to dict

    rule_candidates = get_rule_candidates(query.compound, KB_rules)
    for rule in rule_candidates:
        if rule.direction != "backward":
            continue

        θ_1 = unify(query.compound, rule.consequent.compound, {})
        if θ_1 is None:
            continue

        print(f"Rule matched for backward chaining: {rule}")

        θ_final = dict(θ_1)
        success = True

        for conjunct in rule.antecedent:
            sub_query = ds.Query(conjunct.compound)
            sub_θ = ASK(sub_query, KB_facts, KB_rules)
            if sub_θ == "FAIL":
                success = False
                break
            θ_final.update(sub_θ)

        if success:
            new_fact = ds.Fact(subst(list(θ_final.items()), rule.consequent.compound))
            if new_fact not in KB_facts:
                KB_facts.append(new_fact)
                print(f"Derived new fact (backward): {new_fact}")
            return θ_final

    print(f"ASK failed for query: {query.compound}")
    return "FAIL"

