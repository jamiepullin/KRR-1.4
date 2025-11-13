#Part II - Background ---------------

class Term: #basic data type
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.name == other.name
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __hash__(self):
        return hash(self.name)

class Atom(Term):
    pass

class Variable(Term):
    def __init__(self, name):
        if not (name[0].isupper() or (name[0] == "_")):
            raise ValueError("Unsuitable variable form. Variable must be uppercase letter or begin with '_'.")
        Term.__init__(self, name)


class Number(Term):
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Number term must be type int or float")
        self.value = value
        Term.__init__(self, str(value)) #value/string value

class Compound(Term): #relation between arguments
    def __init__(self, op: Atom, args):
        if not isinstance(args, list):
            raise TypeError("args must be of type list")
        for arg in args:
            if not isinstance(arg, Term):
                raise TypeError(f"Elements must be of type Term")
        self.op = op
        self.args = args
        Term.__init__(self, op.name)

    def __repr__(self):
        args_str = ", ".join((repr(arg) for arg in self.args))
        return f"{self.op.name}({args_str})"

    def __eq__(self, other):
        if isinstance(other, Compound):
            return self.op == other.op and self.args == other.args
        return False


class TList(Term):
    def __init__(self, elements):
        if not isinstance(elements, list):
            raise TypeError("List must contain only Term objects")
        for element in elements:
            if not isinstance(element, Term):
                raise TypeError(f"Elements must be of type Term")
        self.elements = elements
        Term.__init__(self, "TList")

    def __repr__(self):
        elements_str = ", ".join((repr(element) for element in self.elements))
        return f"TList({elements_str})"

class Sentence: #bhulding blocks of KB
    def __init__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"

class Fact(Sentence): #Ground sentence with no variables
    def __init__(self, compound: Compound):
        Sentence.__init__(self)

        if not isinstance(compound, Compound):
            raise TypeError("Fact must encapsulate term of type compound")
        self.compound = compound

    def __repr__(self):
        return f"Fact({repr(self.compound)})"

class Query(Sentence): #Compound allows variables
    def __init__(self, compound: Compound):
        Sentence.__init__(self)

        if not isinstance(compound, Compound):
            raise TypeError("Query must encapsulate term of type compound")
        self.compound = compound

    def __repr__(self):
        return f"Query({repr(self.compound)})"

class Rule(Sentence): #consists of more parts (ant, cons, direction
    def __init__(self, antecedent: list, consequent: Fact, direction):
        Sentence.__init__(self)

        if not isinstance(antecedent, list):
            raise TypeError("Antecedent must be of type list")
        for ant in antecedent:
            if not isinstance(ant, Fact):
                raise TypeError("Antecedent must be of type Fact")

        if not isinstance(consequent, Fact):
            raise TypeError("Consequent must be of type fact")

        if direction not in ("forward", "backward"):
            raise ValueError("Direction must be either forward of backward")

        self.antecedent = antecedent
        self.consequent = consequent
        self.direction = direction

    def __repr__(self):
        ant_str = ", ".join((repr(ant) for ant in self.antecedent))
        direction = "->" if self.direction == "forward" else "<-"
        return f"Rule(({ant_str}, {direction}, {repr(self.consequent)})"