# Item 41: Consider Composing Functionality with Mix-in Classes

# If you find yourself desiring the convenience and encapsulation that
# come with multiple inheritance, but want to avoid the potential headaches,
# consider writing a mix-in instead. A mix-in is a class that
# defines only a small set of additional methods for its child classes to
# provide. Mix-in classes don’t define their own instance attributes nor
# require their __init__ constructor to be called.

# Writing mix-ins is easy because Python makes it trivial to inspect the
# current state of any object, regardless of its type. Dynamic inspection
# means you can write generic functionality just once, in a mix-in, and
# it can then be applied to many other classes. Mix-ins can be composed and
# layered to minimize repetitive code and maximize reuse.
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)
    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output
    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())
# {'value': 10,
#  'left': {'value': 7,
#  'left': None,
#  'right': {'value': 9, 'left': None, 'right': None}},
#  'right': {'value': 13,
#  'left': {'value': 11, 'left': None, 'right': None},
#  'right': None}}

# The best part about mix-ins is that you can make their generic functionality
# pluggable so behaviors can be overridden when required. For
# example, here I define a subclass of BinaryTree that holds a reference
# to its parent. This circular reference would cause the default implementation
# of ToDictMixin.to_dict to loop forever:
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent
# The solution is to override the BinaryTreeWithParent._traverse method
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value # Prevent cycles
        else:
            return super()._traverse(key, value)
root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())
# {'value': 10,
#  'left': {'value': 7,
#  'left': None,
#  'right': {'value': 9,
#  'left': None,
#  'right': None,
#  'parent': 7},
#  'parent': 10},
#  'right': None,
#  'parent': None}

# By defining BinaryTreeWithParent._traverse, I’ve also enabled any
# class that has an attribute of type BinaryTreeWithParent to
# automatically work with the ToDictMixin
class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent
my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict()) # No infinite loop
# {'name': 'foobar',
#  'tree_with_parent': {'value': 9,
#  'left': None,
#  'right': None,
#  'parent': 7}}

# Mix-ins can also be composed together.
import json
class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)
    def to_json(self):
        return json.dumps(self.to_dict())
# Note how the JsonMixin class defines both instance methods and class
# methods. Mix-ins let you add either kind of behavior to subclasses.
# In this example, the only requirements of a JsonMixin subclass are
# providing a to_dict method and taking keyword arguments for
# the __init__ method
class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]
class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed
class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk
serialized = """{
 "switch": {"ports": 5, "speed": 1e9},
 "machines": [
 {"cores": 8, "ram": 32e9, "disk": 5e12},
 {"cores": 4, "ram": 16e9, "disk": 1e12},
 {"cores": 2, "ram": 4e9, "disk": 500e9}
 ]
}"""
deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)

# When you use mix-ins like this, it’s fine if the class you apply
# JsonMixin to already inherits from JsonMixin higher up in the class
# hierarchy. The resulting class will behave the same way, thanks to
# the behavior of super.

# ✦ Avoid using multiple inheritance with instance attributes and
# __init__ if mix-in classes can achieve the same outcome.
# ✦ Use pluggable behaviors at the instance level to provide per-class
# customization when mix-in classes may require it.
# ✦ Mix-ins can include instance methods or class methods, depending
# on your needs.
# ✦ Compose mix-ins to create complex functionality from simple
# behaviors.
