# Item 7: Prefer enumerate Over range

from random import randint
random_bits = 0
for i in range(32):
    if randint(0, 1):
        random_bits |= 1 << i
print(bin(random_bits))

# Often, you’ll want to iterate over a list and also know the
# index of the current item in the list
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i + 1}: {flavor}')
# enumerate wraps any iterator with a lazy generator
# enumerate yields pairs of the loop index and the
# next value from the given iterator
for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')
# can make this even shorter by specifying the number
# from which enumerate should begin counting (1 in this case)
# as the second parameter
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')

# ✦ enumerate provides concise syntax for looping over an iterator and
# getting the index of each item from the iterator as you go.
# ✦ Prefer enumerate instead of looping over a range and indexing into a sequence.
# ✦ You can supply a second parameter to enumerate to specify the number
# from which to begin counting (zero is the default).
