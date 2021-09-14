# Item 19: Never Unpack More Than Three Variables When Functions Return Multiple Values

# Python functions can seemingly return more than one value.
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum
lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]
minimum, maximum = get_stats(lengths)  # Two return values
print(f'Min: {minimum}, Max: {maximum}')
# Min: 60, Max: 73

# The way this works is that multiple values are returned together in a
# two-item tuple. The calling code then unpacks the returned tuple by
# assigning two variables.
first, second = 1, 2
assert first == 1
assert second == 2
def my_function():
    return 1, 2
first, second = my_function()
assert first == 1
assert second == 2

# Multiple return values can also be received by starred expressions
# for catch-all unpacking

def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled
longest, *middle, shortest = get_avg_ratio(lengths)
print(f'Longest:  {longest:>4.0%}')
print(f'Shortest: {shortest:>4.0%}')
# Longest:  108%
# Shortest:  89%

# Now, imagine that the program’s requirements change, and I need to
# also determine the average length, median length, and total population
# size of the alligators.
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count
    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]
    return minimum, maximum, average, median, count
minimum, maximum, average, median, count = get_stats(lengths)
print(f'Min: {minimum}, Max: {maximum}')
print(f'Average: {average}, Median: {median}, Count {count}')
# Min: 60, Max: 73
# Average: 67.5, Median: 68.5, Count 10

# There are two problems with this code. First, all the return values
# are numeric, so it is all too easy to reorder them accidentally
# Second, the line that calls the function and unpacks the values is long,
# and it likely will need to be wrapped in one of a variety of ways
# (due to PEP8 style), which hurts readability
minimum, maximum, average, median, count = get_stats(
    lengths)
minimum, maximum, average, median, count = \
    get_stats(lengths)
(minimum, maximum, average,
 median, count) = get_stats(lengths)
(minimum, maximum, average, median, count
    ) = get_stats(lengths)

# To avoid these problems, you should never use more than three variables
# when unpacking the multiple return values from a function. These could
# be individual values from a three-tuple, two variables and one catch-all
# starred expression, or anything shorter. If you need to unpack more return
# values than that, you’re better off defining a lightweight class or namedtuple
# and having your function return an instance of that instead.

# ✦ You can have functions return multiple values by putting them in a tuple
# and having the caller take advantage of Python’s unpacking syntax.
# ✦ Multiple return values from a function can also be unpacked by catch-all
# starred expressions.
# ✦ Unpacking into four or more variables is error prone and should be avoided;
# instead, return a small class or namedtuple instance.
