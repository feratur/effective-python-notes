# Item 6: Prefer Multiple Assignment Unpacking Over Indexing

item = ('Peanut butter', 'Jelly')
first = item[0]
second = item[1]
print(first, 'and', second)
# Once a tuple is created, you can’t modify it by assigning
# a new value to an index

# Python also has syntax for unpacking, which allows for assigning
# multiple values in a single statement. The patterns that you specify
# in unpacking assignments look a lot like trying to mutate tuples —
# which isn’t allowed — but they actually work quite differently.
item = ('Peanut butter', 'Jelly')
first, second = item  # Unpacking
print(first, 'and', second)
# Peanut butter and Jelly

# The same pattern matching syntax of unpacking works when assigning to
# lists, sequences, and multiple levels of arbitrary iterables within iterables.
favorite_snacks = {
    'salty': ('pretzels', 100),
    'sweet': ('cookies', 180),
    'veggie': ('carrots', 20),
}
((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()
print(f'Favorite {type1} is {name1} with {cals1} calories')
print(f'Favorite {type2} is {name2} with {cals2} calories')
print(f'Favorite {type3} is {name3} with {cals3} calories')

# unpacking can even be used to swap values in place without the need to
# create temporary variables
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                temp = a[i]
                a[i] = a[i-1]
                a[i-1] = temp
names = ['pretzels', 'carrots', 'arugula', 'bacon']
bubble_sort(names)
print(names)
# ['arugula', 'bacon', 'carrots', 'pretzels']

# right side of the assignment (a[i], a[i-1]) is evaluated first, and
# its values are put into a new temporary, unnamed tuple
# (such as ('carrots', 'pretzels') on the first iteration of the loops).
# Then, the unpacking pattern from the left side of the assignment
# (a[i-1], a[i]) is used to receive that tuple value and assign it to
# the variable names a[i-1] and a[i], respectively.

# Another valuable application of unpacking is in the target list of
# for loops and similar constructs, such as comprehensions and
# generator expressions
snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} has {calories} calories')

# Python provides additional unpacking functionality for list construction,
# keyword arguments, multiple return values, and more.

# ✦ Python has special syntax called unpacking for assigning multiple
# values in a single statement.
# ✦ Unpacking is generalized in Python and can be applied to any iterable,
# including many levels of iterables within iterables.
# ✦ Reduce visual noise and increase code clarity by using unpacking to
# avoid explicitly indexing into sequences.
