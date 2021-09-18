# Item 42: Prefer Public Attributes Over Private Ones

# In Python, there are only two types of visibility for a class’s attributes:
# public and private:
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10
    def get_private_field(self):
        return self.__private_field

# Public attributes can be accessed by anyone using the dot operator on
# the object:
foo = MyObject()
assert foo.public_field == 5
# Private fields are specified by prefixing an attribute’s name with a
# double underscore. They can be accessed directly by methods of the
# containing class:
assert foo.get_private_field() == 10
# However, directly accessing private fields from outside the class raises
# an exception:
# foo.__private_field - AttributeError

# Class methods also have access to private attributes because they are
# declared within the surrounding class block:
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71
    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field
bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71

# As you’d expect with private fields, a subclass can’t access its parent
# class’s private fields:
class MyParentObject:
    def __init__(self):
        self.__private_field = 71
class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field
baz = MyChildObject()
# print(baz.get_private_field()) - AttributeError

# The private attribute behavior is implemented with a simple
# transformation of the attribute name. When the Python
# compiler sees private attribute access in methods like
# MyChildObject.get_private_field, it translates the __private_field
# attribute access to use the name _MyChildObject__private_field
# instead.
assert baz._MyParentObject__private_field == 71
print(baz.__dict__)
# {'_MyParentObject__private_field': 71}

# To minimize damage from accessing internals unknowingly, Python
# programmers follow a naming convention defined in the style guide. Fields prefixed by a
# single underscore (like _protected_field) are protected by convention,
# meaning external users of the class should proceed with caution.
class MyBaseClass:
    def __init__(self, value):
        self.__value = value
    def get_value(self):
        return self.__value
class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())

# In general, it’s better to err on the side of allowing subclasses to do
# more by using protected attributes. Document each protected field
# and explain which fields are internal APIs available to subclasses and
# which should be left alone entirely.
class MyClass:
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned in
        # the object it should be treated as immutable.
        self._value = value

# The only time to seriously consider using private attributes is when
# you’re worried about naming conflicts with subclasses. This problem
# occurs when a child class unwittingly defines an attribute that was
# already defined by its parent class:
class ApiClass:
    def __init__(self):
        self._value = 5
    def get(self):
        return self._value
class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # Conflicts
a = Child()
print(f'{a.get()} and {a._value} should be different')
# hello and hello should be different

# This is primarily a concern with classes that are part of a public
# API; the subclasses are out of your control, so you can’t refactor to
# fix the problem. Such a conflict is especially possible with attribute
# names that are very common (like value).
class ApiClass:
    def __init__(self):
        self.__value = 5 # Double underscore
    def get(self):
        return self.__value # Double underscore
class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # OK!
a = Child()
print(f'{a.get()} and {a._value} are different')
# 5 and hello are different

# ✦ Private attributes aren’t rigorously enforced by the Python compiler.
# ✦ Plan from the beginning to allow subclasses to do more with your
# internal APIs and attributes instead of choosing to lock them out.
# ✦ Use documentation of protected fields to guide subclasses instead of
# trying to force access control with private attributes.
# ✦ Only consider using private attributes to avoid naming conflicts
# with subclasses that are out of your control.
