# Item 21: Know How Closures Interact with Variable Scope

def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

# Python supports closures—that is, functions that refer to variables from
# the scope in which they were defined. This is why the helper function is
# able to access the group argument for sort_priority.
#
# Functions are first-class objects in Python, which means you can refer to
# them directly, assign them to variables, pass them as arguments to other
# functions, compare them in expressions and if statements, and so on. This
# is how the sort method can accept a closure function as the key argument.
#
# Python has specific rules for comparing sequences (including tuples). It
# first compares items at index zero; then, if those are equal, it compares
# items at index one; if they are still equal, it compares items at index two,
# and so on. This is why the return value from the helper closure causes the
# sort order to have two distinct groups.

def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True  # Seems simple
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)
# Found: False
# [2, 3, 5, 7, 1, 4, 6, 8]

# Why False?

# When you reference a variable in an expression, the Python interpreter traverses
# the scope to resolve the reference in this order:
# 1. The current function’s scope.
# 2. Any enclosing scopes (such as other containing functions).
# 3. The scope of the module that contains the code (also called the global scope).
# 4. The built-in scope (that contains functions like len and str).
#
# If none of these places has defined a variable with the referenced
# name, then a NameError exception is raised

# Assigning a value to a variable works differently. If the variable is already
# defined in the current scope, it will just take on the new value. If the variable
# doesn’t exist in the current scope, Python treats the assignment as a variable
# definition. Critically, the scope of the newly defined variable is the function
# that contains the assignment.

a = 1
def foo1():
    print(a)
def foo2():
    a = 2
    print(a)
def foo3():
    print(a)
    a = 2
    print(a)
foo1() # prints 1
foo2() # prints 2
# foo3() # Error: a is not defined

def sort_priority2(numbers, group):
    found = False         # Scope: 'sort_priority2'
    def helper(x):
        if x in group:
            found = True  # Scope: 'helper' -- Bad!
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
# this behavior is the intended result: It prevents local variables in a
# function from polluting the containing module

# n Python, there is special syntax for getting data out of a closure.
# The nonlocal statement is used to indicate that scope traversal should
# happen upon assignment for a specific variable name. The only limit is
# that nonlocal won’t traverse up to the module-level scope (to avoid
# polluting globals).
def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found  # Added
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# The nonlocal statement makes it clear when data is being assigned out of
# a closure and into another scope. It’s complementary to the global statement,
# which indicates that a variable’s assignment should go directly into the
# module scope.

# When your usage of nonlocal starts getting complicated, it’s better to wrap
# your state in a helper class.
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True


# ✦ Closure functions can refer to variables from any of the scopes in which they
# were defined.
# ✦ By default, closures can’t affect enclosing scopes by assigning variables.
# ✦ Use the nonlocal statement to indicate when a closure can modify a variable
# in its enclosing scopes.
# ✦ Avoid using nonlocal statements for anything beyond simple functions.
