# Item 30: Consider Generators Instead of Returning Lists

# The simplest choice for a function that produces a sequence of results is to return a list of items.
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = 'Four score and seven years ago...'
result = index_words(address)
print(result[:10])
# [0, 5, 11, 15, 21, 27, 31, 35, 43, 51]

# The first problem is that the code is a bit dense and noisy.
# A better way to write this function is by using a generator.
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


# When called, a generator function does not actually run but instead immediately
# returns an iterator. With each call to the next built-in function, the iterator
# advances the generator to its next yield expression. Each value passed to yield
# by the generator is returned by the iterator to the caller:
it = index_words_iter(address)
print(next(it))
print(next(it))
# 0
# 5

# You can easily convert the iterator returned by the generator to a list by passing
# it to the list built-in function if necessary
result = list(index_words_iter(address))
print(result[:10])
# [0, 5, 11, 15, 21, 27, 31, 35, 43, 51]

# The second problem with index_words is that it requires all results to be stored in
# the list before being returned. For huge inputs, this can cause a program to run out
# of memory and crash.

# In contrast, a generator version of this function can easily be adapted to take inputs
# of arbitrary length due to its bounded memory requirements. For example, here I define
# a generator that streams input from a file one line at a time and yields outputs one word at a time:
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

# The working memory for this function is limited to the maximum length of one line of input.
# with open('address.txt', 'r') as f:
#     it = index_file(f)
#     results = itertools.islice(it, 0, 10)
#     print(list(results))
# [0, 5, 11, 15, 21, 27, 31, 35, 43, 51]

# The only gotcha with defining generators like this is that the callers must be aware that
# the iterators returned are stateful and can’t be reused

# ✦ Using generators can be clearer than the alternative of having a function return a list
# of accumulated results.
# ✦ The iterator returned by a generator produces the set of values passed to yield expressions
# within the generator function’s body.
# ✦ Generators can produce a sequence of outputs for arbitrarily large inputs because their working
# memory doesn’t include all inputs and outputs.
