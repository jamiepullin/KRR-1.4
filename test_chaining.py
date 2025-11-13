import KB
from dataStructures import *
from functions import *

KB_rules = KB.rules

KB_facts = []
print("TELL test")
for fact in KB.facts:
    TELL(fact, KB_facts, KB_rules)

print("\nAll facts after forward chaining:")
for fact in KB_facts:
    print(fact)


print("\n\nASK test\n")
for query in KB.queries:
    print(f"Query: {query.compound}")
    θ = ASK(query, KB_facts, KB_rules)

    if θ == "FAIL" or θ is None:
        print("Result: FAIL\n")
    else:
        # θ is a list of (Variable, value) tuples
        results = {str(var): str(val) for var, val in θ if var in query.compound.args}
        if results:
            print(f"Result substitutions: {results}\n")
        else:
            print("Result: True (no variable substitution needed)\n")



