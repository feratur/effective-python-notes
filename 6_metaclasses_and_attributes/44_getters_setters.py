# Item 44: Use Plain Attributes Instead of Setter and Getter Methods

class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms
    def get_ohms(self):
        return self._ohms
    def set_ohms(self, ohms):
        self._ohms = ohms

# Using these setters and getters is simple, but it’s not Pythonic:
r0 = OldResistor(50e3)
print('Before:', r0.get_ohms())
r0.set_ohms(10e3)
print('After: ', r0.get_ohms())
# Before: 50000.0
# After: 10000.0

r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3

class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0
r1 = Resistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3

# Note that in order for this code to work properly, the names of both the setter
# and the getter methods must match the intended property name
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0
    @property
    def voltage(self):
        return self._voltage
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

# Now, assigning the voltage property will run the voltage setter
# method, which in turn will update the current attribute of the object
# to match:
r2 = VoltageResistance(1e3)
print(f'Before: {r2.current:.2f} amps')
r2.voltage = 10
print(f'After: {r2.current:.2f} amps')
# Before: 0.00 amps
# After: 0.01 amps

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
    @property
    def ohms(self):
        return self._ohms
    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        self._ohms = ohms

# Assigning an invalid resistance to the attribute now raises an 
# exception
r3 = BoundedResistance(1e3)
# r3.ohms = 0 - ValueError

# An exception is also raised if I pass an invalid value to the constructor:
# BoundedResistance(-5) - ValueError

# This happens because BoundedResistance.__init__ calls
# Resistor.__init__, which assigns self.ohms = -5. That assignment
# causes the @ohms.setter method from BoundedResistance to be called,
# and it immediately runs the validation code before object construction has completed.

# I can even use @property to make attributes from parent classes
# immutable:
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
    @property
    def ohms(self):
        return self._ohms
    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms
# Trying to assign to the property after construction raises an exception:
# r4 = FixedResistance(1e3)
# r4.ohms = 2e3
# >>>
# Traceback ...
# AttributeError: Ohms is immutable

# don’t set other attributes in getter property methods
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms
    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms
# Setting other attributes in getter property methods leads to extremely
# bizarre behavior:
r7 = MysteriousResistor(10)
r7.current = 0.01
print(f'Before: {r7.voltage:.2f}')
r7.ohms
print(f'After: {r7.voltage:.2f}')
# Before: 0.00
# After: 0.10

# The biggest shortcoming of @property is that the methods for an attribute
# can only be shared by subclasses. Unrelated classes can’t share
# the same implementation. However, Python also supports descriptors
# (see Item 46: “Use Descriptors for Reusable @property Methods”) that
# enable reusable property logic and many other use cases.

# ✦ Define new class interfaces using simple public attributes and avoid
# defining setter and getter methods.
# ✦ Use @property to define special behavior when attributes are
# accessed on your objects, if necessary.
# ✦ Follow the rule of least surprise and avoid odd side effects in your
# @property methods.
# ✦ Ensure that @property methods are fast; for slow or complex work—
# especially involving I/O or causing side effects—use normal methods instead.
