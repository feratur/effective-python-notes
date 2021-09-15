# Item 28: Avoid More Than Two Control Subexpressions in Comprehensions

# These subexpressions run in the order provided, from left to right
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

squared = [[x**2 for x in row] for row in matrix]
print(squared)
# [[1, 4, 9], [16, 25, 36], [49, 64, 81]]

# my_lists = [
#     [[1, 2, 3], [4, 5, 6]],
#     ...
# ]
# flat = [x for sublist1 in my_lists
#         for sublist2 in sublist1
#         for x in sublist2]

# But this is shorter
# flat = []
# for sublist1 in my_lists:
#     for sublist2 in sublist1:
#         flat.extend(sublist2)

# Comprehensions support multiple if conditions. Multiple conditions at the same loop level have an
# implicit and expression. For example, say that I want to filter a list of numbers to only even values
# greater than 4. These two list comprehensions are equivalent
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]

# Conditions can be specified at each level of looping after the for subexpression.
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)
# [[6], [9]]

# The rule of thumb is to avoid using more than two control subexpres- sions in a comprehension.

# ✦ Comprehensions support multiple levels of loops and multiple con- ditions per loop level.
# ✦ Comprehensions with more than two control subexpressions are very difficult to read and should be avoided.
