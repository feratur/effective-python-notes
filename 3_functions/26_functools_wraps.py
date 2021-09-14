# Item 26: Define Function Decorators with functools.wraps

# Python has special syntax for decorators that can be applied to functions.
# A decorator has the ability to run additional code before and after each call
# to a function it wraps.
# This means decorators can access and modify input arguments, return values,
# and raised exceptions.
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper
# I can apply this decorator to a function by using the @ symbol:
@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))
# Using the @ symbol is equivalent to calling the decorator on the function it wraps
# and assigning the return value to the original name in the same scope:
fibonacci = trace(fibonacci)

# The decorated function runs the wrapper code before and after fibonacci runs.
# It prints the arguments and return value at each level in the recursive stack:
fibonacci(4)
# fibonacci((0,), {}) -> 0
# fibonacci((1,), {}) -> 1
# fibonacci((2,), {}) -> 1
# fibonacci((1,), {}) -> 1
# fibonacci((0,), {}) -> 0
# fibonacci((1,), {}) -> 1
# fibonacci((2,), {}) -> 1
# fibonacci((3,), {}) -> 2
# fibonacci((4,), {}) -> 3

# This works well, but it has an unintended side effect. The value returned
# by the decorator—the function that’s called above—doesn’t think it’s named
# fibonacci:
print(fibonacci)
# <function trace.<locals>.wrapper at 0x108955dc0>

# The trace function returns the wrapper defined within its body.
# help built-in function is useless when called on the decorated fibonacci function.
# It should instead print out the doc- string defined above ('Return the n-th
# Fibonacci number'):
help(fibonacci)
# Help on function wrapper in module __main__:
# wrapper(*args, **kwargs)

# Object serializers break because they can’t determine the location of the original
# function that was decorated
import pickle
# pickle.dumps(fibonacci)
# Traceback ...
# AttributeError: Can't pickle local object 'trace.<locals>.  ̄wrapper'

# The solution is to use the wraps helper function from the functools built-in
# module. This is a decorator that helps you write decorators. When you apply it
# to the wrapper function, it copies all of the important metadata about the inner
# function to the outer function:
from functools import wraps
def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper
@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

help(fibonacci)
# Help on function fibonacci in module __main__:
# fibonacci(n)
#     Return the n-th Fibonacci number

print(pickle.dumps(fibonacci))
# b'\x80\x04\x95\x1a\x00\x00\x00\x00\x00\x00\x00\x8c\x08__main__\  ̄x94\x8c\tfibonacci\x94\x93\x94.'

# Python functions have many other standard attributes (e.g., __name__, __module__,
# __annotations__) that must be preserved to maintain the interface of functions
# in the language. Using wraps ensures that you’ll always get the correct behavior.

# ✦ Decorators in Python are syntax to allow one function to modify another
# function at runtime.
# ✦ Using decorators can cause strange behaviors in tools that do introspection,
# such as debuggers.
# ✦ Use the wraps decorator from the functools built-in module when you define
# your own decorators to avoid issues.
