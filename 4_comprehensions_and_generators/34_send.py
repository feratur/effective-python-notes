# Item 34: Avoid Injecting Data into Generators with send

import math
def wave(amplitude, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output

def transmit(output):
    if output is None:
        print(f'Output is None')
    else:
        print(f'Output: {output:>5.1f}')
def run(it):
    for output in it:
        transmit(output)
run(wave(3.0, 8))
# Output: 0.0
# Output: 2.1
# Output: 3.0
# Output: 2.1
# Output: 0.0
# Output: -2.1
# Output: -3.0
# Output: -2.1

# This works fine for producing basic waveforms, but it can’t be used to
# constantly vary the amplitude of the wave based on a separate input
# (i.e., as required to broadcast AM radio signals). I need a way to
# modulate the amplitude on each iteration of the generator.

# Python generators support the send method, which upgrades yield
# expressions into a two-way channel. The send method can be used to
# provide streaming inputs to a generator at the same time it’s yielding
# outputs.
# Normally, when iterating a generator, the value of the yield
# expression is None:

def my_generator():
    received = yield 1
    print(f'received = {received}')

it = iter(my_generator())
output = next(it) # Get first generator output
print(f'output = {output}')

try:
    next(it) # Run generator until it exits
except StopIteration:
    pass
# output = 1
# received = None

# When I call the send method instead of iterating the generator with a
# for loop or the next built-in function, the supplied parameter becomes
# the value of the yield expression when the generator is resumed. However,
# when the generator first starts, a yield expression has not been
# encountered yet, so the only valid value for calling send initially is
# None (any other argument would raise an exception at runtime):
it = iter(my_generator())
output = it.send(None) # Get first generator output (next(it) will work too)
print(f'output = {output}')
try:
    it.send('hello!') # Send value into the generator
except StopIteration:
    pass
# output = 1
# received = hello!

def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield # Receive initial amplitude
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output # Receive next amplitude

# Then, I need to update the run function to stream the modulating
# amplitude into the wave_modulating generator on each iteration. The
# first input to send must be None, since a yield expression would not
# have occurred within the generator yet:
def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)
run_modulating(wave_modulating(12))
# Output is None
# Output: 0.0
# Output: 3.5
# Output: 6.1
# Output: 2.0
# Output: 1.7
# Output: 1.0
# Output: 0.0
# Output: -5.0
# Output: -8.7
# Output: -10.0
# Output: -8.7
# Output: -5.0

# This works; it properly varies the output amplitude based on the input
# signal. The first output is None, as expected, because a value for the
# amplitude wasn’t received by the generator until after the initial yield
# expression.

def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)
run(complex_wave())
# Output: 0.0
# Output: 6.1
# Output: -6.1
# Output: 0.0
# Output: 2.0
# Output: 0.0
# Output: -2.0
# Output: 0.0
# Output: 9.5
# Output: 5.9
# Output: -5.9
# Output: -9.5

def complex_wave_modulating():
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)
run_modulating(complex_wave_modulating())
# Output is None
# Output: 0.0
# Output: 6.1
# Output: -6.1
# Output is None
# Output: 0.0
# Output: 2.0
# Output: 0.0
# Output: -10.0
# Output is None
# Output: 0.0
# Output: 9.5
# Output: 5.9

# There are many None values in the output! Why does this happen?
# When each yield from expression finishes iterating over a nested
# generator, it moves on to the next one. Each nested generator starts with
# a bare yield expression—one without a value—in order to receive the
# initial amplitude from a generator send method call. This causes the
# parent generator to output a None value when it transitions between
# child generators.
# This means that assumptions about how the yield from and send
# features behave individually will be broken if you try to use them
# together. Although it’s possible to work around this None problem
# by increasing the complexity of the run_modulating function, it’s not
# worth the trouble. It’s already difficult for new readers of the code to
# understand how send works. This surprising gotcha with yield from
# makes it even worse. My advice is to avoid the send method entirely
# and go with a simpler approach.

# The easiest solution is to pass an iterator into the wave function.
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it) # Get next input
        output = amplitude * fraction
        yield output

def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)

def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)
run_cascading()
# Output: 0.0
# Output: 6.1
# Output: -6.1
# Output: 0.0
# Output: 2.0
# Output: 0.0
# Output: -2.0
# Output: 0.0
# Output: 9.5
# Output: 5.9
# Output: -5.9
# Output: -9.5

# The best part about this approach is that the iterator can come from
# anywhere and could be completely dynamic (e.g., implemented using
# a generator function). The only downside is that this code assumes
# that the input generator is completely thread safe, which may not be
# the case. If you need to cross thread boundaries, async functions may
# be a better fit

# ✦ The send method can be used to inject data into a generator by giving
# the yield expression a value that can be assigned to a variable.
# ✦ Using send with yield from expressions may cause surprising
# behavior, such as None values appearing at unexpected times in the
# generator output.
# ✦ Providing an input iterator to a set of composed generators is a better
# approach than using the send method, which should be avoided.
