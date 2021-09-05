# Item 10: Prevent Repetition with Assignment Expressions

# walrus operator—is a new syntax introduced in Python 3.8

# Assignment expressions are useful because they enable you
# to assign variables in places where assignment statements
# are disallowed, such as in the conditional expression of
# an if statement.
# An assignment expression’s value evaluates to whatever was
# assigned to the identifier on the left side of the walrus operator

fresh_fruit = {
    'apple': 10,
    'banana': 8,
    'lemon': 5,
}

def make_lemonade(count):
    ...
def out_of_stock():
    ...

count = fresh_fruit.get('lemon', 0)
if count:
    make_lemonade(count)
else:
    out_of_stock()
# can be rewritten as
if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)
else:
    out_of_stock()

# The assignment expression is first assigning a value to
# the count variable, and then evaluating that value in the
# context of the if statement to determine how to proceed with flow control

def make_cider(count):
    ...

count = fresh_fruit.get('apple', 0)
if count >= 4:
    make_cider(count)
else:
    out_of_stock()
# improving clarity
if (count := fresh_fruit.get('apple', 0)) >= 4:
    make_cider(count)
else:
    out_of_stock()

def slice_bananas(count):
    ...
def make_smoothies(pieces):
    ...

# Emulating switch/case
if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('apple', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('lemon', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = 'Nothing'

# Emulating do/while

def pick_fruit():
    ...
def make_juice(fruit, count):
    ...

bottles = []
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

# ✦ Assignment expressions use the walrus operator (:=) to both assign
# and evaluate variable names in a single expression, thus reducing repetition.
# ✦ When an assignment expression is a subexpression of a larger expression,
# it must be surrounded with parentheses.
# ✦ Although switch/case statements and do/while loops are not availablein Python,
# their functionality can be emulated much more clearly by using assignment expressions.
