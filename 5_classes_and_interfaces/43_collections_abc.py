# Item 43: Inherit from collections.abc for Custom Container Types

# When you’re designing classes for simple use cases like sequences,
# it’s natural to want to subclass Python’s built-in list type directly.
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)
    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts

# By subclassing list, I get all of list’s standard functionality and
# preserve the semantics familiar to all Python programmers. I can define
# additional methods to provide any custom behaviors that I need
foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())
# Length is 7
# After pop: ['a', 'b', 'a', 'c', 'b', 'a']
# Frequency: {'a': 3, 'b': 2, 'c': 1}

# Now, imagine that I want to provide an object that feels like a list
# and allows indexing but isn’t a list subclass.
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
# When you access a sequence item by index
# bar[0] it will be interpreted as bar.__getitem__(0)

class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()
    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'Index {index} is out of range')

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11)))
print('LRR is', tree.left.right.right.value)
print('Index 0 is', tree[0])
print('Index 1 is', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))
# LRR is 7
# Index 0 is 2
# Index 1 is 5
# 11 in the tree? True
# 17 in the tree? False
# Tree is [2, 5, 6, 7, 10, 11, 15]

# The problem is that implementing __getitem__ isn’t enough to provide
# all of the sequence semantics you’d expect from a list instance:
# len(tree)
# >>>
# Traceback ...
# TypeError: object of type 'IndexableNode' has no len()

# The len built-in function requires another special method, named
# __len__, that must have an implementation for a custom sequence
# type:
class SequenceNode(IndexableNode):
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count
tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6,
            right=SequenceNode(7))),
    right=SequenceNode(
        15,
        left=SequenceNode(11))
)
print('Tree length is', len(tree))
# Tree length is 7

# Also missing are the count and index methods that a
# Python programmer would expect to see on a sequence like list or
# tuple.
from collections.abc import Sequence
class BadType(Sequence):
    pass
# foo = BadType()
# >>>
# Traceback ...
# TypeError: Can't instantiate abstract class BadType with 
# ➥abstract methods __getitem__, __len__

# When you do implement all the methods required by an abstract base
# class from collections.abc, as I did above with SequenceNode, it
# provides all of the additional methods, like index and count, for free:
class BetterNode(SequenceNode, Sequence):
    pass
tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))),
    right=BetterNode(
        15,
        left=BetterNode(11))
)
print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))
# Index of 7 is 3
# Count of 10 is 1

# The benefit of using these abstract base classes is even greater for
# more complex container types such as Set and MutableMapping, which
# have a large number of special methods that need to be implemented
# to match Python conventions.
# Beyond the collections.abc module, Python uses a variety of special
# methods for object comparisons and sorting, which may be provided
# by container classes and non-container classes alike.

# ✦ Inherit directly from Python’s container types (like list or dict) for
# simple use cases.
# ✦ Beware of the large number of methods required to implement custom
# container types correctly.
# ✦ Have your custom container types inherit from the interfaces
# defined in collections.abc to ensure that your classes match
# required interfaces and behaviors.
