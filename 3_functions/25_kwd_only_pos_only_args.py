# Item 25: Enforce Clarity with Keyword-Only and Positional-Only Arguments

def safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
# This call ignores the float overflow from division and returns zero:
result = safe_division(1.0, 10**500, True, False)
assert result == 0
# This call ignores the error from dividing by zero and returns infinity:
result = safe_division(1.0, 0, False, True)
assert result == float('inf')

# The problem is that it’s easy to confuse the position of the two Boolean
# arguments that control the exception-ignoring behavior.
# One way to improve the readability of this code is to use keyword arguments.
def safe_division_b(number, divisor,
                    ignore_overflow=False,        # Changed
                    ignore_zero_division=False):  # Changed
    return safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division)

# Then, callers can use keyword arguments to specify which of the ignore flags
# they want to set for specific operations, overriding the default behavior
result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)
result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)
# 0
# inf

# The problem is, since these keyword arguments are optional behavior, there’s
# nothing forcing callers to use keyword arguments for clarity. Even with the new
# definition of safe_division_b, you can still call it the old way with positional
# arguments:
assert safe_division_b(1.0, 10**500, True, False) == 0

# With complex functions like this, it’s better to require that callers are clear
# about their intentions by defining functions with keyword-only arguments. These
# arguments can only be supplied by keyword, never by position.

# The * symbol in the argument list indicates the end of positional arguments and
# the beginning of keyword-only arguments:
def safe_division_c(number, divisor, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    return safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division)
# Now, calling the function with positional arguments for the keyword
# arguments won’t work:
# safe_division_c(1.0, 10**500, True, False) - TypeError
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass  # Expected

# However, a problem still remains with the safe_division_c version of this
# function: Callers may specify the first two required arguments (number and divisor)
# with a mix of positions and keywords
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4

# Later, I may decide to change the names of these first two arguments because of
# expanding needs or even just because my style preferences change:
def safe_division_c(numerator, denominator, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    return safe_division(numerator, denominator,
                  ignore_overflow,
                  ignore_zero_division)
# safe_division_c(number=2, divisor=5) - TypeError

# Python 3.8 introduces a solution to this problem, called positional-only arguments.
# These arguments can be supplied only by position and never by keyword

# The / symbol in the argument list indicates where positional-only arguments end
def safe_division_d(numerator, denominator, /, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    return safe_division(numerator, denominator,
                  ignore_overflow,
                  ignore_zero_division)

assert safe_division_d(2, 5) == 0.4
# But an exception is raised if keywords are used for the positional-only parameters:
# safe_division_d(numerator=2, denominator=5) - TypeError

# Now, I can be sure that the first two required positional arguments in the
# definition of the safe_division_d function are decoupled from callers.

# One notable consequence of keyword- and positional-only arguments is that any
# parameter name between the / and * symbols in the argu- ment list may be passed
# either by position or by keyword (which is the default for all function arguments
# in Python). Depending on your API’s style and needs, allowing both argument passing
# styles can increase readability and reduce noise.
def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,          # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator  # Changed
        return round(fraction, ndigits)     # Changed
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
# Now, I can call this new version of the function in all these different ways,
# since ndigits is an optional parameter that may be passed either by position
# or by keyword:
result = safe_division_e(22, 7)
print(result)
result = safe_division_e(22, 7, 5)
print(result)
result = safe_division_e(22, 7, ndigits=2)
print(result)
# 3.1428571429
# 3.14286
# 3.14

# ✦ Keyword-only arguments force callers to supply certain arguments by keyword
# (instead of by position), which makes the intention of a function call clearer.
# Keyword-only arguments are defined after a single * in the argument list.
# ✦ Positional-only arguments ensure that callers can’t supply certain parameters
# using keywords, which helps reduce coupling. Positional-only arguments are defined
# before a single / in the argument list.
# ✦ Parameters between the / and * characters in the argument list may be supplied
# by position or keyword, which is the default for Python parameters.
