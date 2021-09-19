# Item 46: Use Descriptors for Reusable @property Methods

# The big problem with the @property built-in is reuse. The
# methods it decorates can’t be reused for multiple attributes of the
# same class. They also can’t be reused by unrelated classes.

class Homework:
    def __init__(self):
        self._grade = 0
    @property
    def grade(self):
        return self._grade
    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value
galileo = Homework()
galileo.grade = 95

class Exam:
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0
    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
    @property
    def writing_grade(self):
        return self._writing_grade
    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value
    @property
    def math_grade(self):
        return self._math_grade
    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

# Also, this approach is not general. If I want to reuse this percentage
# validation in other classes beyond homework and exams, I’ll need to
# write the @property boilerplate and _check_grade method over and
# over again.

# The descriptor protocol defines how attribute access is interpreted by
# the language. A descriptor class can provide __get__ and __set__ methods
# that let you reuse the grade validation behavior without boilerplate.
# For this purpose, descriptors are also better than mix-ins because
# they let you reuse the same logic for many different attributes in a
# single class.

# Here, I define a new class called Exam with class attributes that are
# Grade instances. The Grade class implements the descriptor protocol:

class Grade:
    def __get__(self, instance, instance_type):
        ...
    def __set__(self, instance, value):
        ...
class Exam:
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

# When I assign a property
exam = Exam()
exam.writing_grade = 40
# it is interpreted as:
Exam.__dict__['writing_grade'].__set__(exam, 40)
# When I retrieve a property:
exam.writing_grade
# it is interpreted as:
Exam.__dict__['writing_grade'].__get__(exam, Exam)

# What drives this behavior is the __getattribute__ method of object
# (see Item 47: “Use __getattr__, __getattribute__, and __setattr__
# for Lazy Attributes”). In short, when an Exam instance doesn’t have an
# attribute named writing_grade, Python falls back to the Exam class’s
# attribute instead. If this class attribute is an object that has __get__
# and __set__ methods, Python assumes that you want to follow the
# descriptor protocol.

class Grade:
    def __init__(self):
        self._value = 0
    def __get__(self, instance, instance_type):
        return self._value
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value

class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()
first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)
# Writing 82
# Science 99

# But accessing these attributes on multiple Exam instances causes
# unexpected behavior:
second_exam = Exam()
second_exam.writing_grade = 75
print(f'Second {second_exam.writing_grade} is right')
print(f'First {first_exam.writing_grade} is wrong; '
      f'should be 82')
# Second 75 is right
# First 75 is wrong; should be 82

# The problem is that a single Grade instance is shared across all Exam
# instances for the class attribute writing_grade. The Grade instance for
# this attribute is constructed once in the program lifetime, when the
# Exam class is first defined, not each time an Exam instance is created.

class Grade:
    def __init__(self):
        self._values = {}
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

# Memory leak here.
# The _values dictionary holds a reference to
# every instance of Exam ever passed to __set__ over the lifetime of the
# program. This causes instances to never have their reference count
# go to zero, preventing cleanup by the garbage collector.
from weakref import WeakKeyDictionary
class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value
class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()
first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(f'First {first_exam.writing_grade} is right')
print(f'Second {second_exam.writing_grade} is right')
# First 82 is right
# Second 75 is right

# ✦ Reuse the behavior and validation of @property methods by defining
# your own descriptor classes.
# ✦ Use WeakKeyDictionary to ensure that your descriptor classes don’t
# cause memory leaks.
# ✦ Don’t get bogged down trying to understand exactly how
# __getattribute__ uses the descriptor protocol for getting and setting attributes.
