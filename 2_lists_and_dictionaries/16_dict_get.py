# Item 16: Prefer get Over in and KeyError to Handle Missing Dictionary Keys

counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}

key = 'wheat'

# This requires accessing the key two times and assigning it once.
if key in counters:
    count = counters[key]
else:
    count = 0
counters[key] = count + 1

# More efficient approach (requires only one access and one assignment)
try:
    count = counters[key]
except KeyError:
    count = 0
counters[key] = count + 1

# This flow of fetching a key that exists or returning a default value
# is so common that the dict built-in type provides the get method to
# accomplish this task. The second parameter to get is the default value
# to return in the case that the key—the first parameter—isn’t present.

# This also requires only one access and one assignment,
# but it’s much shorter than the KeyError example:
count = counters.get(key, 0)
counters[key] = count + 1

# It’s possible to shorten the in expression and KeyError approaches
# in various ways, but all of these alternatives suffer from requiring
# code duplication for the assignments, which makes them less readable
# and worth avoiding:
if key not in counters:
    counters[key] = 0
counters[key] += 1
if key in counters:
    counters[key] += 1
else:
    counters[key] = 1
try:
    counters[key] += 1
except KeyError:
    counters[key] = 1

# Thus, for a dictionary with simple types, using the get method is the
# shortest and clearest option.

# If you’re maintaining dictionaries of counters like this, it’s worth
# considering the Counter class from the collections built-in module,
# which provides most of the facilities you are likely to need.

# What if the values of the dictionary are a more complex type, like a list?
votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}
key = 'brioche'
who = 'Elmer'
if key in votes:
    names = votes[key]
else:
    votes[key] = names = []
names.append(who)

# The triple assignment statement (votes[key] = names = [])
# populates the key in one line instead of two.

# More efficient:
try:
    names = votes[key]
except KeyError:
    votes[key] = names = []
names.append(who)

# or
names = votes.get(key)
if names is None:
    votes[key] = names = []
names.append(who)

# even shorter
if (names := votes.get(key)) is None:
    votes[key] = names = []
names.append(who)

# The dict type also provides the setdefault method to help shorten
# this pattern even further. setdefault tries to fetch the value of
# a key in the dictionary. If the key isn’t present, the method assigns
# that key to the default value provided. And then the method returns
# the value for that key: either the originally present value or the newly
# inserted default value.
names = votes.setdefault(key, [])
names.append(who)

# This works as expected, and it is shorter than using get with an assignment
# expression. However, the readability of this approach isn’t ideal.

# There’s also one important gotcha: The default value passed to setdefault
# is assigned directly into the dictionary when the key is missing instead
# of being copied.
data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('Before:', data)
value.append('hello')
print('After: ', data)
# Before: {'foo': []}
# After:  {'foo': ['hello']}

# This means that I need to make sure that I’m always constructing a new
# default value for each key I access with setdefault. This leads to a
# significant performance overhead in this example because I have to
# allocate a list instance for each call.

# Why not also use the setdefault method in the first case?
count = counters.setdefault(key, 0)
counters[key] = count + 1
# The problem here is that the call to setdefault is superfluous.
# You always need to assign the key in the dictionary to a new value
# after you increment the counter, so the extra assignment done by
# setdefault is unnecessary. The earlier approach of using get for
# counter updates requires only one access and one assignment,
# whereas using setdefault requires one access and two assignments.

# There are only a few circumstances in which using setdefault is the
# shortest way to handle missing dictionary keys, such as when the
# default values are cheap to construct, mutable, and there’s no potential
# for raising exceptions (e.g., list instances). In these very specific cases,
# it may seem worth accepting the confusing method name setdefault instead of
# having to write more characters and lines to use get. However, often what
# you really should do in these situations is to use defaultdict instead.

# ✦ There are four common ways to detect and handle missing keys in dictionaries:
# using in expressions, KeyError exceptions, the get method, and the setdefault
# method.
# ✦ The get method is best for dictionaries that contain basic types like counters,
# and it is preferable along with assignment expressions when creating dictionary
# values has a high cost or may raise exceptions.
# ✦ When the setdefault method of dict seems like the best fit for your problem,
# you should consider using defaultdict instead.
