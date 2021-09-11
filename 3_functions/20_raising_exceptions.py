# Item 20: Prefer Raising Exceptions to Returning None

def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

# Code using this function can interpret the return value accordingly:
x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print('Invalid inputs')

# Can be problematic in situation like this
x, y = 0, 5
result = careful_divide(x, y)
if not result:
    print('Invalid inputs')  # This runs! But shouldn't

# returning None from a function like careful_divide is error prone

# The first way is to split the return value into a two-tuple
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

success, result = careful_divide(x, y)
if not success:
    print('Invalid inputs')

# can be just as error prone as returning None:
_, result = careful_divide(x, y)
if not result:
    print('Invalid inputs')

# The second, better way to reduce these errors is to never return None for
# special cases. Instead, raise an Exception up to the caller and have the
# caller deal with it.

def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

# The caller no longer requires a condition on the return value of the function.
x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)

# Python’s gradual typing purposefully doesn’t provide a way to indicate when
# exceptions are part of a function’s interface (also known as checked exceptions).
# Instead, you have to document the exception-raising behavior and expect callers
# to rely on that in order to know which Exceptions they should plan to catch.
def careful_divide(a: float, b: float) -> float:
    """Divides a by b.

    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

# ✦ Functions that return None to indicate special meaning are error prone because
# None and other values (e.g., zero, the empty string) all evaluate to False in
# conditional expressions.
# ✦ Raise exceptions to indicate special situations instead of returning None.
# Expect the calling code to handle exceptions properly when they’re documented.
# ✦ Type annotations can be used to make it clear that a function will never return
# the value None, even in special situations.
