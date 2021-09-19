# Item 47: Use __getattr__, __getattribute__, and __setattr__ for Lazy Attributes

# If a class defines __getattr__, that
# method is called every time an attribute can’t be found in an object’s
# instance dictionary:
class LazyRecord:
    def __init__(self):
        self.exists = 5
    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value
# Here, I access the missing property foo. This causes Python to call
# the __getattr__ method above, which mutates the instance dictionary __dict__:
data = LazyRecord()
print('Before:', data.__dict__)
print('foo: ', data.foo)
print('After: ', data.__dict__)
# Before: {'exists': 5}
# foo: Value for foo
# After: {'exists': 5, 'foo': 'Value for foo'}

# Here, I add logging to LazyRecord to show when __getattr__ is actually
# called. Note how I call super().__getattr__() to use the superclass’s
# implementation of __getattr__ in order to fetch the real
# property value and avoid infinite recursion (see Item 40: “Initialize
# Parent Classes with super” for background):
class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* Called __getattr__({name!r}), '
              f'populating instance dictionary')
        result = super().__getattr__(name)
        print(f'* Returning {result!r}')
        return result
data = LoggingLazyRecord()
print('exists: ', data.exists)
print('First foo: ', data.foo)
print('Second foo: ', data.foo)
# exists: 5
# * Called __getattr__('foo'), populating instance dictionary
# * Returning 'Value for foo'
# First foo: Value for foo
# Second foo: Value for foo

# The foo attribute is not in the
# instance dictionary initially, so __getattr__ is called the first time.
# But the call to __getattr__ for foo also does a setattr, which populates
# foo in the instance dictionary. This is why the second time I
# access foo, it doesn’t log a call to __getattr__.

# This behavior is especially helpful for use cases like lazily accessing
# schemaless data. __getattr__ runs once to do the hard work of loading a
# property; all subsequent accesses retrieve the existing result.

# Python has another object
# hook called __getattribute__. This special method is called every
# time an attribute is accessed on an object, even in cases where it does
# exist in the attribute dictionary. 
class ValidatingRecord:
    def __init__(self):
        self.exists = 5
    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        try:
            value = super().__getattribute__(name)
            print(f'* Found {name!r}, returning {value!r}')
            return value
        except AttributeError:
            value = f'Value for {name}'
            print(f'* Setting {name!r} to {value!r}')
            setattr(self, name, value)
            return value
data = ValidatingRecord()
print('exists: ', data.exists)
print('First foo: ', data.foo)
print('Second foo: ', data.foo)
# * Called __getattribute__('exists')
# * Found 'exists', returning 5
# exists: 5
# * Called __getattribute__('foo')
# * Setting 'foo' to 'Value for foo'
# First foo: Value for foo
# * Called __getattribute__('foo')
# * Found 'foo', returning 'Value for foo'
# Second foo: Value for foo

# In the event that a dynamically accessed property shouldn’t exist,
# I can raise an AttributeError to cause Python’s standard missing
# property behavior for both __getattr__ and __getattribute__:
class MissingPropertyRecord:
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError(f'{name} is missing')
        ...
data = MissingPropertyRecord()
# data.bad_name
# Traceback ...
# AttributeError: bad_name is missing

# Python code implementing generic functionality often relies on the
# hasattr built-in function to determine when properties exist, and the
# getattr built-in function to retrieve property values. These functions
# also look in the instance dictionary for an attribute name before calling __getattr__:
data = LoggingLazyRecord() # Implements __getattr__
print('Before: ', data.__dict__)
print('Has first foo: ', hasattr(data, 'foo'))
print('After: ', data.__dict__)
print('Has second foo: ', hasattr(data, 'foo'))
# Before: {'exists': 5}
# * Called __getattr__('foo'), populating instance dictionary
# * Returning 'Value for foo'
# Has first foo: True
# After: {'exists': 5, 'foo': 'Value for foo'}
# Has second foo: True

data = ValidatingRecord() # Implements __getattribute__
print('Has first foo: ', hasattr(data, 'foo'))
print('Has second foo: ', hasattr(data, 'foo'))
# * Called __getattribute__('foo')
# * Setting 'foo' to 'Value for foo'
# Has first foo: True
# * Called __getattribute__('foo')
# * Found 'foo', returning 'Value for foo'
# Has second foo: True

# The __setattr__ method is always called every time an
# attribute is assigned on an instance (either directly or through the
# setattr built-in function):
class SavingRecord:
    def __setattr__(self, name, value):
        # Save some data for the record
        ...
        super().__setattr__(name, value)

class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* Called __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)
data = LoggingSavingRecord()
print('Before: ', data.__dict__)
data.foo = 5
print('After: ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)
# Before: {}
# * Called __setattr__('foo', 5)
# After: {'foo': 5}
# * Called __setattr__('foo', 7)
# Finally: {'foo': 7}

# The problem with __getattribute__ and __setattr__ is that they’re
# called on every attribute access for an object, even when you may not
# want that to happen.
class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = {}
    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        return self._data[name]
data = BrokenDictionaryRecord({'foo': 3})
# data.foo
# * Called __getattribute__('foo')
# * Called __getattribute__('_data')
# * Called __getattribute__('_data')
# * Called __getattribute__('_data')
# ...
# Traceback ...
# RecursionError: maximum recursion depth exceeded while calling 
# ➥a Python object

# The problem is that __getattribute__ accesses self._data, which
# causes __getattribute__ to run again, which accesses self._data
# again, and so on. The solution is to use the super().__getattribute__
# method to fetch values from the instance attribute dictionary. This
# avoids the recursion:
class DictionaryRecord:
    def __init__(self, data):
        self._data = data
    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        data_dict = super().__getattribute__('_data')
        return data_dict[name]
data = DictionaryRecord({'foo': 3})
print('foo: ', data.foo)
# * Called __getattribute__('foo')
# foo: 3

# __setattr__ methods that modify attributes on an object also need to 
# use super().__setattr__ accordingly.

# ✦ Use __getattr__ and __setattr__ to lazily load and save attributes
# for an object.
# ✦ Understand that __getattr__ only gets called when accessing a
# missing attribute, whereas __getattribute__ gets called every time
# any attribute is accessed.
# ✦ Avoid infinite recursion in __getattribute__ and __setattr_
# by using methods from super() (i.e., the object class) to access
# instance attributes.
