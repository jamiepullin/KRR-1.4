import dataStructures as ds
from functions import unify  # your unify code
from functions import print_theta

# --- Helper to create terms easily ---
def V(name):
    return ds.Variable(name)

def A(name):
    return ds.Atom(name)

def C(op, args):
    return ds.Compound(A(op), args)

# --- Test cases ---

def run_tests():
    tests = []

    # 1. UNIFY(2, 2, {}) → {}
    tests.append(("UNIFY(2,2)", ds.Number(2), ds.Number(2), []))

    # 2. UNIFY(aString, aString, {}) → {}
    aString = A("aString")
    tests.append(("UNIFY(aString,aString)", aString, aString, []))

    # 3. UNIFY("New York", "Big Apple", {}) → FAIL
    NY = A("New York")
    BA = A("Big Apple")
    tests.append(("UNIFY('New York','Big Apple')", NY, BA, []))

    # 4. UNIFY(Person, john,{}) → {Person/john}
    Person = V("Person")
    john = A("john")
    tests.append(("UNIFY(Person,john)", Person, john, []))

    # 5. UNIFY(p(X, Y), p(q(a,b), r(c)), {}) → {X/q(a,b), Y/r(c)}
    X = V("X")
    Y = V("Y")
    term1 = C("p", [C("q", [A("a"), A("b")]), C("r", [A("c")])])
    term2 = C("p", [X, Y])
    tests.append(("UNIFY(p(X,Y), p(q(a,b),r(c)))", term2, term1, []))

    # 6. UNIFY(3, A, UNIFY(2, A, {})) → FAIL
    A1 = V("A")
    θ1 = unify(ds.Number(2), A1, [])
    tests.append(("UNIFY(3,A,UNIFY(2,A,{}))", ds.Number(3), A1, θ1))

    # 7. UNIFY(B, A, UNIFY(2, A, {})) → {A/2, B/2}
    B = V("B")
    A2 = V("A")
    θ2 = unify(ds.Number(2), A2, [])
    tests.append(("UNIFY(B,A,UNIFY(2,A,{}))", B, A2, θ2))

    # 8. UNIFY(Y, f(g(Y)), {}) → FAIL
    Y_var = V("Y")
    term = C("f", [C("g", [Y_var])])
    tests.append(("UNIFY(Y,f(g(Y)))", Y_var, term, []))

    # --- Run tests ---
    for desc, x, y, theta in tests:
        print(f"\nTest: {desc}")
        try:
            result = unify(x, y, theta)
            if result is None:
                print("Result: FAIL")
            else:
                print(f"Result: {print_theta(result)}")
        except Exception as e:
            print(f"Result: Exception! {e}")

if __name__ == "__main__":
    run_tests()
