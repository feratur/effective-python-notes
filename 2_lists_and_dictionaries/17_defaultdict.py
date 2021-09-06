# Item 17: Prefer defaultdict Over setdefault to Handle Missing Items in Internal State

visits = {
    'Mexico': {'Tulum', 'Puerto Vallarta'},
    'Japan': {'Hakone'},
}
# I can use the setdefault method to add new cities to the sets, whether
# the country name is already present in the dictionary or not.
visits.setdefault('France', set()).add('Arles')  # Short

if (japan := visits.get('Japan')) is None:       # Long
    visits['Japan'] = japan = set()
japan.add('Kyoto')

# Custom class, incapsulating logic
class Visits:
    def __init__(self):
        self.data = {}
    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)
visits = Visits()
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')
print(visits.data)
# {'Russia': {'Yekaterinburg'}, 'Tanzania': {'Zanzibar'}}

# However, the implementation of the Visits.add method still isn’t ideal.
# The setdefault method is still confusingly named, which makes it more
# difficult for a new reader of the code to immediately understand what’s
# happening. And the implementation isn’t efficient because it constructs
# a new set instance on every call, regardless of whether the given country
# was already present in the data dictionary.

# Luckily, the defaultdict class from the collections built-in module simplifies
# this common use case by automatically storing a default value when a key doesn’t
# exist. All you have to do is provide a function that will return the default
# value to use each time a key is missing
from collections import defaultdict
class Visits:
    def __init__(self):
        self.data = defaultdict(set)
    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('England', 'Bath')
visits.add('England', 'London')
print(visits.data)
# defaultdict(<class 'set'>, {'England': {'London', 'Bath'}})

# Using defaultdict is much better than using setdefault for this type of situation

# ✦ If you’re creating a dictionary to manage an arbitrary set of potential keys,
# then you should prefer using a defaultdict instance from the collections built-in
# module if it suits your problem.
# ✦ If a dictionary of arbitrary keys is passed to you, and you don’t control its
# creation, then you should prefer the get method to access its items. However,
# it’s worth considering using the setdefault method for the few situations in
# which it leads to shorter code.
