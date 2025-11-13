from dataStructures import *
#help(Compound)

print(Fact)

#Terms--------------------------
# Named Individuals
trump = Atom("Trump")
musk = Atom("Musk")
kimk = Atom("KimK")
jimmy_kimmel = Atom("JimmyKimmel")

# Legan Entities
nvidia = Atom("Nvidia")
apple = Atom("Apple")
tesla = Atom("Tesla")

# Places
whitehouse = Atom("Whitehouse")
siliconValley = Atom("SiliconValley")
hollywood = Atom("Hollywood")

# Objects
coffee = Atom("Coffee")
avocado_toast = Atom("AvocadoToast")

# Platforms
twitter = Atom("Twitter")
snl = Atom("SNL")
fox = Atom("Fox")

# Attributes
attention_seeking = Atom("AttentionSeeking")
untouchable = Atom("Untouchable")
climate_friendly = Atom("ClimateFriendly")
coffee_lover = Atom("a coffee lover")
eco_friendly = Atom("EcoFriendly")
tech_savvy = Atom("TechSavvy")

# Variables
X = Variable("X")
Y = Variable("Y")

# Relationships/functions (Compound Ops)
likes = Atom("likes")
endorses = Atom("endorses")
tweets_about = Atom("tweets_about")
consumes = Atom("consumes")
appears_on = Atom("appears_on")
is_probably = Atom("is probably")
lives_in = Atom("lives in")



# Facts----------------------------

facts = [
    Fact(Compound(consumes, [kimk, coffee])),
    Fact(Compound(consumes, [trump, avocado_toast])),
    Fact(Compound(likes, [kimk, apple])),
    Fact(Compound(tweets_about, [jimmy_kimmel, climate_friendly])),
    Fact(Compound(tweets_about, [trump, eco_friendly])),
    Fact(Compound(appears_on, [jimmy_kimmel, snl])),
    Fact(Compound(appears_on, [musk, fox])),
    Fact(Compound(endorses, [musk, tesla]))
]


# Rules -----------------------------

rules = [
    # Anyone who consumes coffee is a coffee lover
    Rule(
        antecedent=[Fact(Compound(consumes, [X, coffee]))],
        consequent=Fact(Compound(is_probably, [X, coffee_lover])),
        direction="forward"
    ),
    # Anyone tweeting about climate-friendly things is eco-friendly
    Rule(
        antecedent=[Fact(Compound(tweets_about, [X, climate_friendly]))],
        consequent=Fact(Compound(is_probably, [X, eco_friendly])),
        direction="forward"
    ),
    # Anyone appearing on snl likes avocado toast
    Rule(
        antecedent=[Fact(Compound(appears_on, [X, snl]))],
        consequent=Fact(Compound(likes, [X, avocado_toast])),
        direction="forward"
    ),
    # Trump tweeting about eco-friendly → attention-seeking
    Rule(
        antecedent=[Fact(Compound(tweets_about, [trump, eco_friendly]))],
        consequent=Fact(Compound(is_probably, [trump, attention_seeking])),
        direction="forward"
    ),
    # trump endorses Tesla → musk untouchable
    Rule(
        antecedent=[Fact(Compound(endorses, [trump, tesla]))],
        consequent=Fact(Compound(is_probably, [musk, untouchable])),
        direction="forward"
    ),

    # someone tweets about climate friendly <- ecofriendly
    Rule(
        antecedent=[Fact(Compound(tweets_about, [X, climate_friendly]))],
        consequent=Fact(Compound(is_probably, [X, eco_friendly])),
        direction="backward"
    ),

    # someone endorses nvidia <- tech_savvy
    Rule(
        antecedent=[Fact(Compound(endorses, [X, Atom(nvidia)]))],
        consequent=Fact(Compound(is_probably, [X, tech_savvy])),
        direction="backward"
    ),

    Rule(
        antecedent=[Fact(Compound(lives_in, [X, siliconValley]))],
        consequent=Fact(Compound(is_probably, [X, tech_savvy])),
        direction="backward"
    )


]

# -------------------
# Queries
# -------------------
queries = [
    Query(Compound(consumes, [X, coffee])),
    Query(Compound(tweets_about, [X, eco_friendly])),
    Query(Compound(likes, [X, avocado_toast])),
    Query(Compound(appears_on, [X, snl])),
    Query(Compound(likes, [trump, attention_seeking])),
    Query(Compound(likes, [musk, untouchable])),
    Query(Compound(likes, [trump, untouchable]))
]

# -------------------
# Debug Harness
# -------------------
if __name__ == "__main__":
    print("=== ALL FACTS ===")
    for f in facts:
        print(f"repr: {repr(f)} | str: {str(f)}")
        if isinstance(f.compound, Compound):
            print("  operator:", f.compound.op)
            print("  args:", [str(a) for a in f.compound.args])
    print("\n=== ALL RULES ===")
    for r in rules:
        print(r)
    print("\n=== ALL QUERIES ===")
    for q in queries:
        print(q)