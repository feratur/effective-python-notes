# Item 9: Avoid else Blocks After for and while Loops

# You can put an else block immediately after a loop’s repeated interior block
for i in range(3):
    print('Loop', i)
else:
    print('Else block!')
# Loop 0
# Loop 1
# Loop 2
# Else block!

# else block runs immediately after the loop finishes
# else from try/except/else means "Do this if there was no exception to handle"

# a new programmer might assume that the else part of for/else means
# “Do this if the loop wasn’t completed.” In reality, it does exactly the opposite.
# Using a break statement in a loop actually skips the else block

for i in range(3):
    print('Loop', i)
    if i == 1:
        break
else:
    print('Else block!')
# Loop 0
# Loop 1

# Another surprise is that the else block runs immediately
# if you loop over an empty sequence

for x in []:
    print('Never runs')
else:
    print('For Else block!')
# For Else block!


# The else block also runs when while loops are initially False:
while False:
    print('Never runs')
else:
    print('While Else block!')
# While Else block!

# The rationale for these behaviors is that else blocks after
# loops are useful when using loops to search for something.

# The else block runs when the numbers are coprime because
# the loop doesn’t encounter a break:
a=4
b=9
for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')
# Testing 2
# Testing 3
# Testing 4
# Coprime

# But such code is difficult to comprehend

# The first approach is to return early when I find the condition
# I’m looking for. I return the default outcome if I fall through the loop:
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True
assert coprime(4, 9)
assert not coprime(3, 6)
# The second way is to have a result variable that indicates
# whether I’ve found what I’m looking for in the loop.
# I break out of the loop as soon as I find something:
def coprime_alternate(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime
assert coprime_alternate(4, 9)
assert not coprime_alternate(3, 6)

# ✦ Python has special syntax that allows else blocks to immediately
# follow for and while loop interior blocks.
# ✦ The else block after a loop runs only if the loop body did not
# encounter a break statement.
# ✦ Avoid using else blocks after loops because their behavior isn’t
# intuitive and can be confusing.
