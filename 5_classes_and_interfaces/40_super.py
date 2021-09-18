# Item 40: Initialize Parent Classes with super

class MyBaseClass:
    def __init__(self, value):
        self.value = value
class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

# If a class is affected by multiple inheritance,
# calling the superclasses’ __init__ methods directly can
# lead to unpredictable behavior. One problem is that the
# __init__ call order isn’t specified across all subclasses.
class TimesTwo:
    def __init__(self):
        self.value *= 2
class PlusFive:
    def __init__(self):
        self.value += 5
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)
foo = OneWay(5)
print('First ordering value is (5 * 2) + 5 =', foo.value)
# First ordering value is (5 * 2) + 5 = 15

# Here’s another class that defines the same parent classes but in a
# different ordering (PlusFive followed by TimesTwo instead of the other
# way around)
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)
bar = AnotherWay(5)
print('Second ordering value is', bar.value)
# Second ordering value is 15

# PlusFive.__init__ and TimesTwo.__init__—in the same order as before
# which means this class’s behavior doesn’t match the order of the parent
# classes in its definition. The conflict here between the inheritance
# base classes and the __init__ calls is hard to spot, which makes this
# especially difficult for new readers of the code to understand

# Another problem occurs with diamond inheritance. Diamond inheritance
# happens when a subclass inherits from two separate classes
# that have the same superclass somewhere in the hierarchy. Diamond
# inheritance causes the common superclass’s __init__ method to
# run multiple times, causing unexpected behavior.
class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7
class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value)
foo = ThisWay(5)
print('Should be (5 * 7) + 9 = 44 but is', foo.value)
# Should be (5 * 7) + 9 = 44 but is 14

# The call to the second parent class’s constructor, PlusNine.__init__,
# causes self.value to be reset back to 5 when MyBaseClass.__init__ gets
# called a second time. That results in the calculation of self.value to be
# 5 + 9 = 14

# To solve these problems, Python has the super built-in function and
# standard method resolution order (MRO). super ensures that common
# superclasses in diamond hierarchies are run only once.
# The MRO defines the ordering in which superclasses are initialized,
# following an algorithm called C3 linearization.
class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7
class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9
# Now, the top part of the diamond, MyBaseClass.__init__, is run only a
# single time. The other parent classes are run in the order specified in
# the class statement:
class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)
foo = GoodWay(5)
print('Should be 7 * (5 + 9) = 98 and is', foo.value)
# Should be 7 * (5 + 9) = 98 and is 98

# Shouldn’t TimesSevenCorrect.__init__ have run first? Shouldn’t the result be
# (5 * 7) + 9 = 44? The answer is no. This ordering matches what the
# MRO defines for this class. The MRO ordering is available on a class
# method called mro:
mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())
print(mro_str)
# <class '__main__.GoodWay'>
# <class '__main__.TimesSevenCorrect'>
# <class '__main__.PlusNineCorrect'>
# <class '__main__.MyBaseClass'>
# <class 'object'>

# When I call GoodWay(5), it in turn calls TimesSevenCorrect.__init__,
# which calls PlusNineCorrect.__init__, which calls MyBaseClass.__
# init__. Once this reaches the top of the diamond, all of the initialization
# methods actually do their work in the opposite order from how
# their __init__ functions were called. MyBaseClass.__init__ assigns
# value to 5. PlusNineCorrect.__init__ adds 9 to make value equal 14.
# TimesSevenCorrect.__init__ multiplies it by 7 to make value equal 98.

# Besides making multiple inheritance robust, the call to super().
# __init__ is also much more maintainable than calling
# MyBaseClass.__init__ directly from within the subclasses. I could
# later rename MyBaseClass to something else or have TimesSevenCorrect
# and PlusNineCorrect inherit from another superclass without having
# to update their __init__ methods to match.

# The super function can also be called with two parameters: first the
# type of the class whose MRO parent view you’re trying to access, and
# then the instance on which to access that view. Using these optional
# parameters within the constructor looks like this
class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
        self.value /= 3

# However, these parameters are not required for object instance initialization.
# Python’s compiler automatically provides the correct
# parameters (__class__ and self) for you when super is called with
# zero arguments within a class definition. This means all three of
# these usages are equivalent:
class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)
        self.value /= 3
class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value /= 3
assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3

# The only time you should provide parameters to super is in situations
# where you need to access the specific functionality of a superclass’s
# implementation from a child class (e.g., to wrap or reuse 
# functionality).

# ✦ Python’s standard method resolution order (MRO) solves the problems
# of superclass initialization order and diamond inheritance.
# ✦ Use the super built-in function with zero arguments to initialize
# parent classes.
