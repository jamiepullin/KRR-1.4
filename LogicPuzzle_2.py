import dataStructures as ds
from functions import unify

class LogicPuzzle_2:

    def __init__(self, term_domain, term_range, op):
        self.possibilities = {ds.Term(x): set(ds.Term(y) for y in term_range) for x in term_domain}
        self.op = op

        self.uniqueness_domain = {ds.Term(x): True for x in term_domain}  # one place per person
        self.uniqueness_range = {ds.Term(y): True for y in term_range}    # one person per place

    def _uniqueness(self):
        changed = True
        while changed:
            changed = False

            for x, options in self.possibilities.items():
                if self.uniqueness_domain[x] and len(options) == 1:
                    y = next(iter(options))
                    for other_x in self.possibilities:
                        if other_x != x and y in self.possibilities[other_x]:
                            self.possibilities[other_x].remove(y)
                            changed = True

            for y in self.uniqueness_range:
                if not self.uniqueness_range[y]:
                    continue
                owners = [x for x, options in self.possibilities.items() if y in options]
                if len(owners) == 1:
                    only_owner = owners[0]
                    for other_y in self.possibilities[only_owner].copy():
                        if other_y != y:
                            self.possibilities[only_owner].remove(other_y)
                            changed = True

    def ADD(self, fact: ds.Fact):
        x, y = fact.compound.args
        if y not in self.possibilities[x]:
            print(f"ADD ignored (contradiction): {fact}")
            return
        print(f"ADD: {fact}")
        self.possibilities[x] = {y}
        self._uniqueness()

    def REMOVE_FACT(self, person_name, place_name):
        x = ds.Term(person_name)
        y = ds.Term(place_name)
        if y in self.possibilities[x]:
            self.possibilities[x].remove(y)
            print(f"Removed possibility: {x} cannot live in {y}")
        self._uniqueness()

    def show(self):
        print("Current possibilities:")
        for x, options in self.possibilities.items():
            print(f"  {x}: {[str(o) for o in options]}")
        print()


puzzle1 = LogicPuzzle_2(
    term_domain=["trump", "musk", "kimk"],
    term_range=["whitehouse", "hollywood", "silicon_valley"],
    op=ds.Atom("lives_in")
)

puzzle1.show()

print("Clue 1: Musk lives in Silicon Valley.")
puzzle1.ADD(ds.Fact(ds.Compound(puzzle1.op, [ds.Atom("musk"), ds.Atom("silicon_valley")])))
puzzle1.show()

print("Clue 2: Trump does not live in Hollywood.")
puzzle1.REMOVE_FACT("trump", "hollywood")
puzzle1.show()


