# Item 33: Compose Multiple Generators with yield from

def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0

# To create the final animation, I need to combine move and pause
# together to produce a single sequence of onscreen deltas.
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta

def render(delta):
    print(f'Delta: {delta:.1f}')
    # Move the images onscreen

def run(func):
    for delta in func():
        render(delta)

run(animate)
# Delta: 5.0
# Delta: 5.0
# Delta: 5.0
# Delta: 5.0
# Delta: 0.0
# Delta: 0.0
# Delta: 0.0
# Delta: 3.0
# Delta: 3.0

# The problem with this code is the repetitive nature of the animate function.
# The solution to this problem is to use the yield from expression.
# This advanced generator feature allows you to yield all values from
# a nested generator before returning control to the parent generator.
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)

run(animate_composed)
# Delta: 5.0
# Delta: 5.0
# Delta: 5.0
# Delta: 5.0
# Delta: 0.0
# Delta: 0.0
# Delta: 0.0
# Delta: 3.0
# Delta: 3.0

# yield from essentially causes the Python interpreter to handle the nested for loop
# and yield expression boilerplate for you, which results in better performance.
import timeit
def child():
    for i in range(1_000_000):
        yield i
def slow():
    for i in child():
        yield i
def fast():
    yield from child()
baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f'Manual nesting {baseline:.2f}s')
comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f'Composed nesting {comparison:.2f}s')
reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} less time')
# Manual nesting 4.02s
# Composed nesting 3.47s
# 13.5% less time

# ✦ The yield from expression allows you to compose multiple nested
# generators together into a single combined generator.
# ✦ yield from provides better performance than manually iterating
# nested generators and yielding their outputs.
