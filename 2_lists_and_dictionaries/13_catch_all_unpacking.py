# Item 13: Prefer Catch-All Unpacking Over Slicing

car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
# One limitation of basic unpacking is that you must know
# the length of the sequences you’re unpacking in advance.
# oldest, second_oldest = car_ages_descending raises ValueError

oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)
# Possible, but noisy

# Python supports catch-all unpacking through a starred expression.
# This syntax allows one part of the unpacking assignment to receive
# all values that didn’t match any other part of the unpacking pattern.
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# A starred expression may appear in any position, so you can get
# the benefits of catch-all unpacking anytime you need to extract one slice
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)
*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)
# 20 0 [19, 15, 9, 8, 7, 6, 4, 1]
# 0 1 [20, 19, 15, 9, 8, 7, 6, 4]

# However, to unpack assignments that contain a starred expression,
# you must have at least one required part, or else you’ll get a SyntaxError.
# You can’t use a catch-all expression on its own:
# *others = car_ages_descending

# You also can’t use multiple catch-all expressions in a single-level unpacking pattern:
# first, *middle, *second_middle, last = [1, 2, 3, 4]

# But it is possible to use multiple starred expressions in an unpacking assignment
# statement, as long as they’re catch-alls for different parts of the multilevel
# structure being unpacked.
car_inventory = {
    'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
    'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}
((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()
print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')
# Best at Downtown is Silver Shadow, 2 others
# Best at Airport is Skyline, 3 others

# Starred expressions become list instances in all cases. If there are no
# leftover items from the sequence being unpacked, the catch-all part will
# be an empty list. This is especially useful when you’re processing a sequence
# that you know in advance has at least N elements
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)
# 1 2 []

# You can also unpack arbitrary iterators with the unpacking syntax.
def generate_csv():
    yield ('Date', 'Make', 'Model', 'Year', 'Price')
    yield ('12-12-2012', 'Volkswagen' , 'Tiguan', '2012', '2000000')

# Too noisy:
all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print('CSV Header:', header)
print('Row count: ', len(rows))

# Clearer:
it = generate_csv()
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))

# Because a starred expression is always turned into a list,
# unpacking an iterator also risks the potential of using up
# all of the memory on your computer and causing your program
# to crash. So you should only use catch-all unpacking on iterators
# when you have good reason to believe that the result data will all fit in memory.

# ✦ Unpacking assignments may use a starred expression to catch all values
# that weren’t assigned to the other parts of the unpacking pattern into a list.
# ✦ Starred expressions may appear in any position, and they will always
# become a list containing the zero or more values they receive.
# ✦ When dividing a list into non-overlapping pieces, catch-all unpacking
# is much less error prone than slicing and indexing.
