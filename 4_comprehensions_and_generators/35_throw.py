# Item 35: Avoid Causing State Transitions in Generators with throw

# throw method for re-raising Exception instances within generator functions
#
# When the method is called, the next occurrence of a yield expression
# re-raises the provided Exception instance after its output is received
# instead of continuing normally

class MyError(Exception):
    pass
def my_generator():
    yield 1
    yield 2
    yield 3
it = my_generator()
print(next(it)) # Yield 1
print(next(it)) # Yield 2
try:
    print(it.throw(MyError('test error')))
except MyError as e:
    print(e)
# 1
# 2
# Traceback ...
# MyError: test error

# When you call throw, the generator function may catch the injected
# exception with a standard try/except compound statement that surrounds
# the last yield expression that was executed
def my_generator():
    yield 1
    try:
        yield 2
    except MyError:
        print('Got MyError!')
    else:
        yield 3
    yield 4
it = my_generator()
print(next(it)) # Yield 1
print(next(it)) # Yield 2
print(it.throw(MyError('test error')))
# 1
# 2
# Got MyError!
# 4

# This functionality provides a two-way communication channel
# between a generator and its caller that can be useful in certain situation
class Reset(Exception):
    pass
def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period
# In this code, whenever the Reset exception is raised by the yield
# expression, the counter resets itself to its original period
def check_for_reset():
    # Poll for external event
    ...
def announce(remaining):
    print(f'{remaining} ticks remaining')
def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)
run()
# 3 ticks remaining
# 2 ticks remaining
# 1 ticks remaining
# 0 ticks remaining

# This code works as expected, but it’s much harder to read than necessary.
# The various levels of nesting required to catch StopIteration
# exceptions or decide to throw, call next, or announce make the code noisy.

# A simpler approach to implementing this functionality is to define a
# stateful closure using an iterable container object
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period
    def reset(self):
        self.current = self.period
    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current
# Now much simpler
def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)
run()
# I suggest that you avoid using throw entirely and instead use
# an iterable class if you need this type of exceptional behavior.

# ✦ The throw method can be used to re-raise exceptions within
# generators at the position of the most recently executed yield
# expression.
# ✦ Using throw harms readability because it requires additional nesting
# and boilerplate in order to raise and catch exceptions.
# ✦ A better way to provide exceptional behavior in generators is to use
# a class that implements the __iter__ method along with methods to
# cause exceptional state transitions.
